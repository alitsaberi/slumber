import inspect
from abc import ABC, abstractmethod
from time import sleep
from typing import Annotated, Literal

from loguru import logger
from playsound3 import playsound
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    FilePath,
)
from pyttsx3 import Engine

from slumber.dag.units.home_lucid_dreaming.cueing import deliver_auditory_cue
from slumber.sources.zmax import (
    LED_MAX_INTENSITY,
    LED_MIN_INTENSITY,
    STIMULATION_MAX_DURATION,
    STIMULATION_MIN_DURATION,
    LEDColor,
    ZMax,
    is_connected,
)
from slumber.utils.helpers import (
    MAX_VOLUME,
    MIN_VOLUME,
    create_enum_by_name_resolver,
    get_system_volume,
    set_system_volume,
)
from slumber.utils.text2speech import text2speech


class Action(BaseModel, ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> None: ...


class ReadText(Action):
    type: Literal["ReadText"] = "ReadText"
    text: str = Field(min_length=1)

    def __call__(self, text2speech_engine: Engine) -> None:
        text2speech(self.text, engine=text2speech_engine)


class SemanticAudioCue(ReadText):
    type: Literal["SemanticAudioCue"] = "SemanticAudioCue"
    volume_increase: float = Field(ge=MIN_VOLUME, le=MAX_VOLUME)

    def __call__(
        self, text2speech_engine: Engine, minimum_subjective_audio_intensity: float
    ) -> None:
        volume = minimum_subjective_audio_intensity + self.volume_increase
        if volume > MAX_VOLUME:
            logger.info(
                f"Volume increase ({self.volume_increase})"
                f" would exceed maximum volume ({MAX_VOLUME})."
            )
            volume = MAX_VOLUME

        deliver_auditory_cue(
            text=self.text,
            volume=volume,
            engine=text2speech_engine,
        )


class VibrationCue(Action):
    type: Literal["VibrationCue"] = "VibrationCue"
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
    repetitions: int = Field(gt=0)

    def __call__(self, zmax: ZMax) -> None:
        zmax.vibrate(
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
        )


class LightCue(VibrationCue):
    type: Literal["LightCue"] = "LightCue"
    led_color: Annotated[
        LEDColor, BeforeValidator(create_enum_by_name_resolver(LEDColor))
    ]
    led_intensity_increase: int = Field(ge=0, lt=100)
    alternate_eyes: bool = False

    def __call__(self, zmax: ZMax, min_subjective_light_intensity: int) -> None:
        intensity = min_subjective_light_intensity + self.led_intensity_increase
        if intensity > LED_MAX_INTENSITY:
            logger.info(
                f"LED intensity increase ({self.led_intensity_increase})"
                f" would exceed maximum intensity ({LED_MAX_INTENSITY})."
            )
            intensity = LED_MAX_INTENSITY

        zmax.stimulate(
            led_color=self.led_color,
            led_intensity=intensity,
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
            alternate_eyes=self.alternate_eyes,
            vibration=False,
        )


class Pause(Action):
    type: Literal["Pause"] = "Pause"
    duration: int = Field(gt=0)

    def __call__(self) -> None:
        sleep(self.duration)


class PlayAudioFile(Action):
    type: Literal["PlayAudioFile"] = "PlayAudioFile"
    file_path: FilePath
    volume_increase: float = Field(ge=MIN_VOLUME, le=MAX_VOLUME)

    def __call__(self, minimum_subjective_audio_intensity: float) -> None:
        volume = minimum_subjective_audio_intensity + self.volume_increase
        if volume > MAX_VOLUME:
            logger.info(
                f"Volume increase ({self.volume_increase})"
                f" would exceed maximum volume ({MAX_VOLUME})."
            )
            volume = MAX_VOLUME

        old_system_volume = get_system_volume()
        logger.debug(f"Setting system volume to {volume} from {old_system_volume}")
        set_system_volume(volume)

        logger.disable("playsound3")  # Disable logging for playsound3
        try:
            playsound(self.file_path)
        finally:
            logger.enable("playsound3")  # Re-enable logging

        logger.debug(f"Setting system volume to {old_system_volume} from {volume}")
        set_system_volume(old_system_volume)


Protocol = list[
    Annotated[
        ReadText | SemanticAudioCue | VibrationCue | LightCue | Pause | PlayAudioFile,
        Field(discriminator="type"),
    ]
]


class CognitiveTrainingConfig(BaseModel):
    zmax: Annotated[ZMax, AfterValidator(is_connected)]
    text2speech_engine: Engine
    min_subjective_light_intensity: int = Field(
        ge=LED_MIN_INTENSITY, le=LED_MAX_INTENSITY
    )
    minimum_subjective_audio_intensity: float = Field(ge=MIN_VOLUME, le=MAX_VOLUME)

    model_config = ConfigDict(arbitrary_types_allowed=True)


def execute_cognitive_training(
    protocol: Protocol,
    config: CognitiveTrainingConfig,
) -> None:
    if not protocol:
        raise ValueError("Protocol cannot be empty")

    available_kwargs = config.model_dump()

    total_actions = len(protocol)
    for i, action in enumerate(protocol):
        try:
            logger.info(f"Executing action {i+1}/{total_actions}: {action!r}")
            required_params = inspect.signature(action).parameters
            action_kwargs = {
                k: v for k, v in available_kwargs.items() if k in required_params
            }
            logger.debug(f"Action kwargs: {action_kwargs}")
            action(**action_kwargs)
        except Exception as e:
            logger.error(f"Failed to execute action {action}: {e}")
            raise
