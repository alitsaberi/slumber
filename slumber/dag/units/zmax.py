import asyncio
from collections.abc import AsyncGenerator
from functools import cached_property
from typing import Annotated

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import AfterValidator, ConfigDict

from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import SAMPLE_RATE as ZMAX_SAMPLE_RATE
from slumber.sources.zmax import DataType, ZMax, is_connected
from slumber.utils.data import Data
from slumber.utils.helpers import enum_by_name_validator


class Settings(PydanticSettings):
    zmax: Annotated[ZMax, AfterValidator(is_connected)]
    data_types: list[Annotated[DataType, enum_by_name_validator(DataType)]]
    buffer_size: int = 10 * ZMAX_SAMPLE_RATE  # 10 seconds
    retry_delay: int = 5

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def channel_names(self) -> list[str]:
        return [data_type.name for data_type in self.data_types]


class State(ez.State):
    buffer: list[np.ndarray]


class ZMaxDataReceiver(ez.Unit):
    SETTINGS = Settings
    STATE = State
    OUTPUT_DATA = ez.OutputStream(Data)

    def initialize(self) -> None:
        self.STATE.buffer = []

    @ez.publisher(OUTPUT_DATA)
    async def collect(self) -> AsyncGenerator:
        while True:
            try:
                sample = self.SETTINGS.zmax.read(self.SETTINGS.data_types)
            except TimeoutError:
                logger.warning(
                    "Timed out while waiting for data from ZMax."
                    f"Retrying in {self.SETTINGS.retry_delay} seconds..."
                )
                await asyncio.sleep(self.SETTINGS.retry_delay)
                continue
            except ConnectionError:
                logger.error("Connection to ZMax lost. Reconnecting...")
                self.SETTINGS.zmax.connect()
                continue

            self.STATE.buffer(sample)

            if len(self.STATE.buffer) >= self.SETTINGS.buffer_size:
                yield (
                    self.OUTPUT_DATA,
                    Data(
                        np.array(self.STATE.buffer),
                        sample_rate=ZMAX_SAMPLE_RATE,
                        channel_names=self.SETTINGS.channel_names,
                    ),
                )
                self.STATE.buffer = []
