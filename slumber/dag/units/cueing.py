import asyncio
from collections.abc import AsyncGenerator
from typing import Annotated, Any

import ezmsg.core as ez
from loguru import logger
import pyttsx3
from pydantic import BaseModel, BeforeValidator, Field, field_serializer, model_validator

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

    def increment(self) -> None:
        old_value = self.value
        self.value = min(self.max, self.value + self.step)
        logger.info(f"Incremented {self} from {old_value}")

    def decrement(self) -> None:
        old_value = self.value
        self.value = max(self.min, self.value - self.step)
        logger.info(f"Decremented {self} from {old_value}")


# TODO: Add validations for intensity attributes for each type of cueing


class VibrationCueingConfig(BaseModel):
    intensity: CueIntensityConfig
    on_duration: int = Field(
        ge=STIMULATION_MIN_DURATION, le=STIMULATION_MAX_DURATION
    )  # 10 units = 1000 ms
    off_duration: int = Field(
        ge=STIMULATION_MIN_DURATION, le=STIMULATION_MAX_DURATION
    )  # 10 units = 1000 ms


class VisualCueingConfig(VibrationCueingConfig):
    intensity: CueIntensityConfig
    led_color: Annotated[
        LEDColor, BeforeValidator(create_enum_by_name_resolver(LEDColor))
    ] = LEDColor.RED
    alternate_eyes: bool = False
    repetitions: int = Field(
        ge=STIMULATION_MIN_REPETITIONS, le=STIMULATION_MAX_REPETITIONS
    )


class AudioCueingConfig(BaseModel):
    intensity: CueIntensityConfig
    text: str = Field(min_length=1)
    voice: str | None = Field(None, min_length=1)
    rate: float = Field(gt=0)


class AudioIntensityConfig(CueIntensityConfig):
    engine: pyttsx3.Engine = Field(repr=False)

    def increment(self) -> None:
        super().increment()
        self._sync_engine_volume()

    def decrement(self) -> None:
        super().decrement()
        self._sync_engine_volume()

    def _sync_engine_volume(self) -> None:
        self.engine.setProperty("volume", self.value)
        
    @field_serializer("engine")
    def serialize_engine(self, engine: pyttsx3.Engine, _info):
        return {
            "volume": self.engine.getProperty("volume"),
            "rate": self.engine.getProperty("rate"),
            "voice": self.engine.getProperty("voice"),
        }


class Settings(PydanticSettings):
    visual_cueing: VisualCueingConfig
    vibration_cueing: VibrationCueingConfig
    audio_cueing: AudioCueingConfig
    enabled: bool = True
    increase_intensity: bool = True
    enabled_check_interval: float = Field(gt=0.0)
    cueing_interval: float = Field(ge=0.0)


class State(ez.State):
    enabled: bool
    increase_intensity: bool
    visual_intensity: CueIntensityConfig
    vibration_intensity: CueIntensityConfig
    audio_intensity: AudioIntensityConfig


class Cueing(ez.Unit):
    SETTINGS = Settings
    STATE = State

    ENABLE_SIGNAL = ez.InputStream(bool)
    ENABLE_INCREASE_INTENSITY_SIGNAL = ez.InputStream(bool)
    DECREASE_INTENSITY_SIGNAL = ez.InputStream(bool)

    ZMAX_STIMULATION_SIGNAL = ez.OutputStream(dict[str, Any])

    async def initialize(self) -> None:
        self.STATE.enabled = self.SETTINGS.enabled
        self.STATE.increase_intensity = self.SETTINGS.increase_intensity
        self.STATE.visual_intensity = CueIntensityConfig.model_validate(
            self.SETTINGS.visual_cueing.intensity
        )
        self.STATE.vibration_intensity = CueIntensityConfig.model_validate(
            self.SETTINGS.vibration_cueing.intensity
        )
        self.STATE.audio_intensity = AudioIntensityConfig.model_validate(
            self.SETTINGS.audio_cueing.intensity,
            engine=init_text2speech_engine(
                rate=self.SETTINGS.audio_cueing.rate,
                volume=self.SETTINGS.audio_cueing.intensity.value,
                voice=self.SETTINGS.audio_cueing.voice,
            ),
        )

    async def shutdown(self) -> None:
        self.STATE.audio_intensity.engine.stop()

    @ez.subscriber(ENABLE_SIGNAL)
    async def update_enabled(self, signal: bool) -> None:
        self.STATE.enabled = signal
        logger.info(f"Cueing is {'' if signal else 'not'}enabled")

    @ez.subscriber(ENABLE_INCREASE_INTENSITY_SIGNAL)
    async def update_increase_intensity(self, signal: bool) -> None:
        self.STATE.increase_intensity = signal
        logger.info(f"Increase intensity is {'' if signal else 'not'}enabled")

    @ez.subscriber(DECREASE_INTENSITY_SIGNAL)
    async def decrease_intensity(self, _: bool) -> None:
        self.STATE.visual_intensity.decrement()
        self.STATE.vibration_intensity.decrement()
        self.STATE.audio_intensity.decrement()

    @ez.publisher(ZMAX_STIMULATION_SIGNAL)
    async def run(self) -> AsyncGenerator:
        while True:
            if not self.STATE.enabled:
                logger.debug("Cueing is disabled")
                await asyncio.sleep(self.SETTINGS.enabled_check_interval)
                continue

            visual_cueing_signal = self._generate_visual_cueing_signal()
            logger.debug(f"Visual cueing signal: {visual_cueing_signal}")
            yield (self.ZMAX_STIMULATION_SIGNAL, visual_cueing_signal)
            await asyncio.sleep(self.SETTINGS.cueing_interval)

            if not self.STATE.enabled:
                continue

            logger.debug(f"Auditory cueing: {self.SETTINGS.audio_cueing.text}. Engine: {self.STATE.audio_intensity.model_dump(include={"engine"})}"))
            text2speech(
                text=self.SETTINGS.audio_cueing.text,
                engine=self.STATE.audio_intensity.engine,
            )

            if not self.STATE.enabled:
                continue

            vibration_cueing_signal = self._generate_vibration_cueing_signal()
            logger.debug(f"Vibration cueing signal: {vibration_cueing_signal}")
            yield (self.ZMAX_STIMULATION_SIGNAL, vibration_cueing_signal)
            await asyncio.sleep(self.SETTINGS.cueing_interval)

            if self.STATE.increase_intensity:
                self.STATE.vibration_intensity.increment()
                self.STATE.vibration_intensity.increment()
                self.STATE.audio_intensity.increment()
                
    def _generate_visual_cueing_signal(self) -> dict[str, Any]:
        return {
            "led_color": self.SETTINGS.visual_cueing.led_color,
            "repetitions": self.SETTINGS.visual_cueing.repetitions,
            "on_duration": self.SETTINGS.visual_cueing.on_duration,
            "off_duration": self.SETTINGS.visual_cueing.off_duration,
            "vibration": False,
            "led_intensity": self.STATE.visual_intensity.value,
            "alternate_eyes": self.SETTINGS.visual_cueing.alternate_eyes,
        }
        
    def _generate_vibration_cueing_signal(self) -> dict[str, Any]:
        return {
            "led_color": LEDColor.OFF,
            "repetitions": self.STATE.vibration_intensity.value,
            "on_duration": self.SETTINGS.vibration_cueing.on_duration,
            "off_duration": self.SETTINGS.vibration_cueing.off_duration,
            "vibration": True,
        }
