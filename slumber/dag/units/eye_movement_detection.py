from collections.abc import AsyncGenerator
from dataclasses import asdict

import ezmsg.core as ez
from loguru import logger
from pydantic import Field

from slumber.dag.utils import PydanticSettings
from slumber.processing.eye_movement import (
    DEFAULTS,
    MovementEvent,
    detect_lr_eye_movements,
)
from slumber.utils.data import Data


class Settings(PydanticSettings):
    left_eeg_label: str
    right_eeg_label: str
    difference_threshold: float = Field(DEFAULTS["difference_threshold"], gt=0)
    min_same_event_gap: float = Field(DEFAULTS["min_same_event_gap"], gt=0)
    max_sequence_gap: float = Field(DEFAULTS["max_sequence_gap"], gt=0)
    low_cutoff: float = Field(DEFAULTS["low_cutoff"], gt=0)
    high_cutoff: float = Field(DEFAULTS["high_cutoff"], gt=0)
    # TODO: add cross field validations


class EyeMovementDetection(ez.Unit):
    SETTINGS = Settings

    INPUT = ez.InputStream(Data)
    EYE_MOVEMENTS = ez.OutputStream(list[MovementEvent])

    @ez.subscriber(INPUT)
    @ez.publisher(EYE_MOVEMENTS)
    async def detect_eye_movements(self, data: Data) -> AsyncGenerator:
        eye_movements = detect_lr_eye_movements(data, **asdict(self.SETTINGS))
        logger.debug(f"Eye movements: {eye_movements}")
        yield (self.EYE_MOVEMENTS, eye_movements)
