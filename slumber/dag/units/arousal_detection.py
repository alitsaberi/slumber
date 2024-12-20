from collections.abc import AsyncGenerator
from dataclasses import asdict

import ezmsg.core as ez
from loguru import logger
from pydantic import Field, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.processing.arousal_detection import DEFAULTS, detect_arousals
from slumber.utils.data import Data, Event


class Settings(PydanticSettings):
    wake_n1_threshold: float = Field(
        default=DEFAULTS["wake_n1_threshold"], ge=0.0, le=1.0
    )
    min_duration: float = Field(default=DEFAULTS["min_duration"], gt=0.0)
    max_duration: float = Field(default=DEFAULTS["max_duration"], gt=0.0)
    merge_gap: float = Field(default=DEFAULTS["merge_gap"], gt=0.0)
    smoothing_window: float = Field(default=DEFAULTS["smoothing_window"], ge=0.0)
    min_transition_increase: float = Field(
        default=DEFAULTS["min_transition_increase"], ge=0.0, le=1.0
    )
    gap_threshold_factor: float = Field(
        default=DEFAULTS["gap_threshold_factor"], ge=0.0, le=1.0
    )

    @model_validator(mode="after")
    def validate_max_duration(self) -> "Settings":
        if self.max_duration <= self.min_duration:
            raise ValueError("max_duration must be greater than min_duration")
        return self


class ArousalDetection(ez.Unit):
    SETTINGS = Settings

    INPUT = ez.InputStream(Data)
    OUTPUT = ez.OutputStream(list[Event])

    @ez.subscriber(INPUT)
    @ez.publisher(OUTPUT)
    async def detect(self, scores: Data) -> AsyncGenerator:
        arousal_events = detect_arousals(
            scores,
            **asdict(self.SETTINGS),
        )

        logger.debug(f"Arousal events: {arousal_events}")

        yield (
            self.OUTPUT,
            arousal_events,
        )
