import asyncio
from collections.abc import AsyncGenerator
from typing import Annotated

import ezmsg.core as ez
import pyttsx3
from loguru import logger
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_serializer,
    model_validator,
)

from slumber.dag.units.event_logger import Event
from slumber.dag.units.home_lucid_dreaming.master import EventType
from slumber.dag.units.zmax import ZMaxStimulationSignal
from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import (
    STIMULATION_MAX_DURATION,
    STIMULATION_MAX_REPETITIONS,
    STIMULATION_MIN_DURATION,
    STIMULATION_MIN_REPETITIONS,
    LEDColor,
)
from slumber.utils.helpers import create_enum_by_name_resolver
from slumber.utils.text2speech import (
    init_text2speech_engine,
    text2speech,
)


class CueIntensityConfig(BaseModel):
    value: int
    max: int
    min: int
    step: int = Field(ge=1)

    @model_validator(mode="after")
    def validate(self) -> "CueIntensityConfig":
        if not (self.min <= self.max):
            raise ValueError("min must be less than or equal to max")

        if not (self.min <= self.value <= self.max):
            raise ValueError("value must be between min and max")

        return self

    def adjust(self, increment: bool) -> None:
        new_value = (
            min(self.max, self.value + self.step)
            if increment
            else max(self.min, self.value - self.step)
        )
        if new_value != self.value:
            action = "Incrementing" if increment else "Decrementing"
            logger.info(f"{action} {self!r} to {new_value}.")
            self.value = new_value


# TODO: Add validations for intensity attributes for each type of cueing


class AudioIntensityConfig(CueIntensityConfig):
    engine: pyttsx3.Engine = Field(repr=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def adjust(self, increment: bool) -> None:
        super().adjust(increment)
        self.engine.setProperty("volume", self.value / 100)

    @field_serializer("engine")
    def serialize_engine(self, engine: pyttsx3.Engine, _info):
        return {
            "volume": engine.getProperty("volume"),
            "rate": engine.getProperty("rate"),
            "voice": engine.getProperty("voice"),
        }


class TactileCueingConfig(BaseModel):
    intensity: CueIntensityConfig
    on_duration: int = Field(
        ge=STIMULATION_MIN_DURATION,
        le=STIMULATION_MAX_DURATION,
        description="Duration of the on state in units of 100 ms",
    )
    off_duration: int = Field(
        ge=STIMULATION_MIN_DURATION,
        le=STIMULATION_MAX_DURATION,
        description="Duration of the off state in units of 100 ms",
    )


class VisualCueingConfig(TactileCueingConfig):
    led_color: Annotated[
        LEDColor, BeforeValidator(create_enum_by_name_resolver(LEDColor))
    ] = LEDColor.RED
    alternate_eyes: bool = False
    repetitions: int = Field(
        ge=STIMULATION_MIN_REPETITIONS, le=STIMULATION_MAX_REPETITIONS
    )


class AuditoryCueingConfig(BaseModel):
    intensity: CueIntensityConfig
    text: str = Field(min_length=1)
    voice: str | None = Field(None, min_length=1)
    rate: float = Field(gt=0)


class Settings(PydanticSettings):
    visual_cueing: VisualCueingConfig
    tactile_cueing: TactileCueingConfig
    auditory_cueing: AuditoryCueingConfig
    enabled: bool = True
    increase_intensity: bool = True
    enabled_check_interval: float = Field(gt=0.0)
    cueing_interval: float = Field(ge=0.0)


class State(ez.State):
    enabled: bool
    increase_intensity: bool
    light_intensity: CueIntensityConfig
    vibration_intensity: CueIntensityConfig
    audio_intensity: AudioIntensityConfig


class Cueing(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT_ENABLE_SIGNAL = ez.InputStream(bool)
    INPUT_ENABLE_INCREASE_INTENSITY_SIGNAL = ez.InputStream(bool)
    INPUT_ADJUST_INTENSITY_SIGNAL = ez.InputStream(bool)

    OUTPUT_ZMAX_STIMULATION_SIGNAL = ez.OutputStream(ZMaxStimulationSignal)
    OUTPUT_LOG_EVENT = ez.OutputStream(Event)

    async def initialize(self) -> None:
        self.STATE.enabled = self.SETTINGS.enabled
        self.STATE.increase_intensity = self.SETTINGS.increase_intensity
        self.STATE.light_intensity = CueIntensityConfig.model_validate(
            self.SETTINGS.visual_cueing.intensity
        )
        self.STATE.vibration_intensity = CueIntensityConfig.model_validate(
            self.SETTINGS.tactile_cueing.intensity
        )
        self.STATE.audio_intensity = AudioIntensityConfig(
            **self.SETTINGS.auditory_cueing.intensity.model_dump(),
            engine=init_text2speech_engine(
                rate=self.SETTINGS.auditory_cueing.rate,
                volume=self.SETTINGS.auditory_cueing.intensity.value,
                voice=self.SETTINGS.auditory_cueing.voice,
            ),
        )

    async def shutdown(self) -> None:
        try:
            self.STATE.audio_intensity.engine.stop()
        except AttributeError as e:
            logger.error(e)
            pass

    @ez.subscriber(INPUT_ENABLE_SIGNAL)
    async def update_enabled(self, signal: bool) -> None:
        if signal != self.STATE.enabled:
            logger.info(f"{'Enabling' if signal else 'Disabling'} cueing")

        self.STATE.enabled = signal

    @ez.subscriber(INPUT_ENABLE_INCREASE_INTENSITY_SIGNAL)
    async def update_increase_intensity(self, signal: bool) -> None:
        if signal != self.STATE.increase_intensity:
            logger.info(f"{'Enabling' if signal else 'Disabling'} increase intensity")
        self.STATE.increase_intensity = signal

    @ez.subscriber(INPUT_ADJUST_INTENSITY_SIGNAL)
    async def adjust_intensity(self, increment: bool) -> None:
        self._adjust_intensity(increment)

    @ez.publisher(OUTPUT_ZMAX_STIMULATION_SIGNAL)
    @ez.publisher(OUTPUT_LOG_EVENT)
    async def run(self) -> AsyncGenerator:
        while True:
            if not self.STATE.enabled:
                logger.info(
                    "Cueing is disabled. Trying again in"
                    f" {self.SETTINGS.enabled_check_interval} second."
                )
                await asyncio.sleep(self.SETTINGS.enabled_check_interval)
                continue

            visual_cueing_signal = self._generate_visual_cueing_signal()
            logger.debug(f"Visual cueing signal: {visual_cueing_signal}")
            yield (
                self.OUTPUT_LOG_EVENT,
                Event(
                    type=EventType.VISUAL_CUE, value=self.STATE.light_intensity.value
                ),
            )
            yield (self.OUTPUT_ZMAX_STIMULATION_SIGNAL, visual_cueing_signal)
            await asyncio.sleep(self.SETTINGS.cueing_interval)

            if not self.STATE.enabled:
                logger.info("Cueing is disabled. Stopping cueing.")
                continue

            logger.debug(
                f"Auditory cueing: {self.SETTINGS.auditory_cueing.text}."
                f" Engine: {self.STATE.audio_intensity.model_dump(include={'engine'})}"
            )
            yield (
                self.OUTPUT_LOG_EVENT,
                Event(
                    type=EventType.AUDITORY_CUE, value=self.STATE.audio_intensity.value
                ),
            )
            text2speech(
                self.SETTINGS.auditory_cueing.text, self.STATE.audio_intensity.engine
            )
            await asyncio.sleep(self.SETTINGS.cueing_interval)

            if not self.STATE.enabled:
                logger.info("Cueing is disabled. Stopping cueing.")
                continue

            vibration_cueing_signal = self._generate_vibration_cueing_signal()
            logger.debug(f"Vibration cueing signal: {vibration_cueing_signal}")
            yield (
                self.OUTPUT_LOG_EVENT,
                Event(
                    type=EventType.TACTILE_CUE,
                    value=self.STATE.vibration_intensity.value,
                ),
            )
            yield (self.OUTPUT_ZMAX_STIMULATION_SIGNAL, vibration_cueing_signal)
            await asyncio.sleep(self.SETTINGS.cueing_interval)

            if self.STATE.increase_intensity:
                self._adjust_intensity(increment=True)

    def _generate_visual_cueing_signal(self) -> ZMaxStimulationSignal:
        return ZMaxStimulationSignal(
            led_color=self.SETTINGS.visual_cueing.led_color,
            repetitions=self.SETTINGS.visual_cueing.repetitions,
            on_duration=self.SETTINGS.visual_cueing.on_duration,
            off_duration=self.SETTINGS.visual_cueing.off_duration,
            vibration=False,
            led_intensity=self.STATE.light_intensity.value,
            alternate_eyes=self.SETTINGS.visual_cueing.alternate_eyes,
        )

    def _generate_vibration_cueing_signal(self) -> ZMaxStimulationSignal:
        return ZMaxStimulationSignal(
            led_color=LEDColor.OFF,
            repetitions=self.STATE.vibration_intensity.value,
            on_duration=self.SETTINGS.tactile_cueing.on_duration,
            off_duration=self.SETTINGS.tactile_cueing.off_duration,
            vibration=True,
        )

    def _adjust_intensity(self, increment: bool) -> None:
        self.STATE.light_intensity.adjust(increment)
        self.STATE.vibration_intensity.adjust(increment)
        self.STATE.audio_intensity.adjust(increment)
