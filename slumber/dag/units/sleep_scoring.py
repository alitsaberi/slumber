from collections.abc import AsyncGenerator
from dataclasses import asdict
from pathlib import Path

import ezmsg.core as ez
from loguru import logger
import numpy as np
from pydantic import Field

from slumber.dag.utils import PydanticSettings
from slumber.processing.sleep_scoring import UTimeModel, score
from slumber.utils.data import Data


class ModelConfig(PydanticSettings):
    model_dir: Path
    weight_file_name: str | None = None
    n_periods: int | None = Field(gt=0)
    n_samples_per_prediction: int = Field(1, gt=0)


class Settings(PydanticSettings):
    model: ModelConfig
    channel_groups: list[list[int | str]] | None = None
    arg_max: bool = True


class State(ez.State):
    model: UTimeModel


class SleepScoring(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT = ez.InputStream(Data)
    OUTPUT_SCORES = ez.OutputStream(Data)

    async def initialize(self) -> None:
        self.STATE.model = UTimeModel(**asdict(self.SETTINGS.model))
        logger.info(f"Loaded model from {self.SETTINGS.model.model_dir}")

    @ez.subscriber(INPUT)
    @ez.publisher(OUTPUT_SCORES)
    async def score_sleep(self, data: Data) -> AsyncGenerator:
        logger.debug(f"Scoring {data}")
        scores = score(
            data,
            self.STATE.model,
            channel_groups=self.SETTINGS.channel_groups,
            arg_max=self.SETTINGS.arg_max,
        )
        
        logger.debug(f"Sleep scores: {scores}")

        yield (self.OUTPUT_SCORES, scores)
