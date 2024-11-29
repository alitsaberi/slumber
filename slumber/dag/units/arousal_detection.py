from collections.abc import AsyncGenerator

import ezmsg.core as ez
from loguru import logger

from slumber.dag.utils import PydanticSettings
from slumber.processing.arousal_detection import detect_arousals
from slumber.utils.data import Data


class Settings(PydanticSettings):
    wake_n1_threshold: float = 0.4
    min_duration: float = 3.0
    max_duration: float = 15.0
    merge_gap: float = 5.0
    smoothing_window: float = 0.0
    min_transition_increase: float = 0.2
    gap_threshold_factor: float = 0.8


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
