import inspect
import sys
from abc import ABC, abstractmethod
from collections.abc import Sequence
from time import sleep
from typing import Annotated, Any

from loguru import logger
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
)
from pyttsx3 import Engine

from slumber.sources.zmax import LEDColor, ZMax, is_connected
from slumber.utils.helpers import (
    create_enum_by_name_resolver,
    get_class_by_name,
)
from slumber.utils.text2speech import text2speech


class Action(BaseModel, ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> None: ...


class ReadTextAction(Action):
    text: str = Field(min_length=1)

    def execute(self, text2speech_engine: Engine) -> None:
        text2speech(self.text, engine=text2speech_engine)


class SemanticAudioCueAction(ReadTextAction):
    volume_increase: float = Field(ge=0.0, le=1.0)

    def execute(self, text2speech_engine: Engine, min_subjective_volume: float) -> None:
        engine_volume = text2speech_engine.getProperty("volume")
        text2speech_engine.setProperty(
            "volume", min_subjective_volume + self.volume_increase
        )
        super().execute(text2speech_engine)
        text2speech_engine.setProperty("volume", engine_volume)


class VibrationCueAction(Action):
    on_duration: int = Field(gt=0)
    off_duration: int = Field(gt=0)
    repetitions: int = Field(gt=0)

    def execute(self, zmax: ZMax) -> None:
        zmax.vibrate(
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
        )


class LightCueAction(VibrationCueAction):
    led_color: Annotated[
        LEDColor, BeforeValidator(create_enum_by_name_resolver(LEDColor))
    ]
    led_intensity_increase: int = Field(ge=0, lt=100)
    alternate_eyes: bool = False

    def execute(self, zmax: ZMax, min_subjective_light_intensity: int) -> None:
        zmax.stimulate(
            led_color=self.led_color,
            led_intensity=min_subjective_light_intensity + self.led_intensity_increase,
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
            alternate_eyes=self.alternate_eyes,
            vibration=False,
        )


class PauseAction(Action):
    duration: int = Field(gt=0)

    def execute(self) -> None:
        sleep(self.duration)


def create_action(action: str, parameters: dict[str, Any] | None = None) -> Action:
    try:
        action = get_class_by_name(action, sys.modules[__name__], Action)
    except AttributeError as e:
        raise ValueError(f"Invalid action: {action}") from e
    parameters = parameters or {}
    return action.model_validate(parameters)


class CognitiveTrainingConfig(BaseModel):
    zmax: Annotated[ZMax, AfterValidator(is_connected)]
    text2speech_engine: Engine
    min_subjective_light_intensity: int = Field(ge=1, le=100)
    min_subjective_volume: float = Field(ge=0.0, le=1.0)

    model_config = ConfigDict(arbitrary_types_allowed=True)


def execute_cognitive_training(
    protocol: Sequence[Action],
    config: CognitiveTrainingConfig,
) -> None:
    if not protocol:
        raise ValueError("Protocol cannot be empty")

    available_kwargs = config.model_dump()

    total_actions = len(protocol)
    for i, action in enumerate(protocol, 1):
        try:
            logger.info(
                f"Executing action {i}/{total_actions}: {action.__class__.__name__}"
            )
            required_params = inspect.signature(action.execute).parameters
            action_kwargs = {
                k: v for k, v in available_kwargs.items() if k in required_params
            }
            logger.debug(f"Action kwargs: {action_kwargs}")
            action.execute(**action_kwargs)
        except Exception as e:
            logger.error(f"Failed to execute action {action}: {e}")
            raise
