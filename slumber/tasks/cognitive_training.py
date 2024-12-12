from abc import ABC, abstractmethod
from enum import Enum
from time import time
from typing import Any

import pyttsx3
from pydantic import BaseModel
from pyttsx3 import Engine

from slumber import CONFIGS_DIR
from slumber.sources.zmax import LEDColor, ZMax
from slumber.utils.helpers import load_yaml, text2speech


class Action(BaseModel, ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> None: ...


class ReadTextAction(Action):
    text: str

    def execute(self, text2speech_engine: Engine, **kwargs) -> None:
        text2speech(self.text, engine=text2speech_engine)


class SemanticAudioCueAction(ReadTextAction):
    volume_increase: float = 0.0

    def execute(
        self, text2speech_engine: Engine, min_subjective_volume: float, **kwargs
    ) -> None:
        engine_volume = text2speech_engine.getProperty("volume")
        text2speech_engine.setProperty(
            "volume", min_subjective_volume + self.volume_increase
        )
        super().execute(text2speech_engine)
        text2speech_engine.setProperty("volume", engine_volume)


class LightCueAction(Action):
    led_color: LEDColor
    led_intensity_increase: int
    on_duration: int
    off_duration: int
    repetitions: int
    alternate_eyes: bool = False

    def execute(
        self, zmax: ZMax, min_subjective_light_intensity: int, **kwargs
    ) -> None:
        zmax.stimulate(
            led_color=self.led_color,
            led_intensity=min_subjective_light_intensity + self.led_intensity_increase,
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
            alternate_eyes=self.alternate_eyes,
            vibration=False,
        )


class VibrationCueAction(Action):
    on_duration: int
    off_duration: int
    repetitions: int

    def execute(self, zmax: ZMax, **kwargs) -> None:
        zmax.vibrate(
            on_duration=self.on_duration,
            off_duration=self.off_duration,
            repetitions=self.repetitions,
        )


class PauseAction(Action):
    duration: int

    def execute(self, **kwargs) -> None:
        time.sleep(self.duration)


class ActionType(Enum):
    READ_TEXT = ReadTextAction
    SEMANTIC_AUDIO_CUE = SemanticAudioCueAction
    LIGHT_CUE = LightCueAction
    VIBRATION_CUE = VibrationCueAction
    PAUSE = PauseAction


def create_action(action: str, parameters: dict[str, Any] | None = None) -> Action:
    action_type = ActionType[action]
    parameters = parameters or {}
    return action_type.value.model_validate(parameters)


def execute_cognitive_training(
    protocol: list[Action],
    zmax: ZMax,
    text2speech_engine: Engine,
    min_subjective_light_intensity: int,
    min_subjective_volume: float,
) -> None:
    if not protocol:
        raise ValueError("Protocol cannot be empty")

    for action in protocol:
        action.execute(
            zmax=zmax,
            text2speech_engine=text2speech_engine,
            min_subjective_light_intensity=min_subjective_light_intensity,
            min_subjective_volume=min_subjective_volume,
        )


if __name__ == "__main__":
    config_file = CONFIGS_DIR / "lucid_dreaming" / "short_cognitive_training.yaml"
    config = load_yaml(config_file)
    protocol = [create_action(**action_config) for action_config in config]

    with ZMax(ip="127.0.0.1", port=8000) as zmax:
        text2speech_engine = pyttsx3.init()

        execute_cognitive_training(
            protocol=protocol,
            zmax=zmax,
            text2speech_engine=text2speech_engine,
            min_subjective_light_intensity=50,
            min_subjective_volume=0.5,
        )
