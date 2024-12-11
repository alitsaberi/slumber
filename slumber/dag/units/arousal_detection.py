from collections.abc import AsyncGenerator

import ezmsg.core as ez
from loguru import logger
from pydantic import Field, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.processing.arousal_detection import detect_arousals
from slumber.utils.data import Data


class Settings(PydanticSettings):
    wake_n1_threshold: float = Field(default=0.4, ge=0.0, le=1.0)
    min_duration: float = Field(default=3.0, gt=0.0)
    max_duration: float = Field(default=15.0, gt=0.0)
    merge_gap: float = Field(default=5.0, gt=0.0)
    smoothing_window: float = Field(default=5.0, ge=0.0)
    min_transition_increase: float = Field(default=0.2, ge=0.0, le=1.0)
    gap_threshold_factor: float = Field(default=0.8, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_max_duration(self) -> "Settings":
        if self.max_duration <= self.min_duration:
            raise ValueError("max_duration must be greater than min_duration")
        return self


class ArousalDetection(ez.Unit):
    SETTINGS = Settings

    INPUT_SCORES = ez.InputStream(Data)
    AROUSAL_INTERVALS = ez.OutputStream(list[tuple[int, int]])

    @ez.subscriber(INPUT_SCORES)
    @ez.publisher(AROUSAL_INTERVALS)
    async def detect(self, scores: Data) -> AsyncGenerator:
        arousal_intervals = detect_arousals(
            scores,
            wake_n1_threshold=self.SETTINGS.wake_n1_threshold,
            min_duration=self.SETTINGS.min_duration,
            max_duration=self.SETTINGS.max_duration,
            merge_gap=self.SETTINGS.merge_gap,
            smoothing_window=self.SETTINGS.smoothing_window,
            min_transition_increase=self.SETTINGS.min_transition_increase,
            gap_threshold_factor=self.SETTINGS.gap_threshold_factor,
        )

        logger.debug(f"Arousal intervals: {arousal_intervals}")

        yield (
            self.AROUSAL_INTERVALS,
            arousal_intervals,
        )
