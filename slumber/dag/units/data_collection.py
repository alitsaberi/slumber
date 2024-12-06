from collections.abc import AsyncGenerator
from time import sleep
from typing import Any

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import field_validator

from slumber import settings
from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import SAMPLE_RATE as ZMAX_SAMPLE_RATE
from slumber.sources.zmax import DataType, ZMax
from slumber.utils.data import Data


class ZMaxConfig(PydanticSettings):
    ip: str
    port: int
    retry_attempts: int = settings["zmax"]["retry_attempts"]
    retry_delay: int = settings["zmax"]["retry_delay"]
    socket_timeout: int = settings["zmax"]["socket_timeout"]


class Settings(PydanticSettings):
    zmax_config: ZMaxConfig
    data_types: list[DataType] | None = None
    buffer_size: int = 10 * ZMAX_SAMPLE_RATE  # 10 seconds
    retry_delay: int = 5

    @field_validator("data_types", mode="before")
    @classmethod
    def resolve_data_types(cls, v: Any) -> Any:
        if v is None:
            return list(DataType)

        if isinstance(v, list) and any(isinstance(item, str) for item in v):
            return [DataType[name] for name in v]

        return v


class ZMaxDataCollection(ez.Unit):
    SETTINGS = Settings
    OUTPUT_DATA = ez.OutputStream(Data)

    def initialize(self) -> None:
        zmax_config = self.SETTINGS.zmax_config
        self._zmax = ZMax(
            zmax_config.ip, zmax_config.port, socket_timeout=zmax_config.socket_timeout
        )
        self._zmax.connect(
            retry_attempts=zmax_config.retry_attempts,
            retry_delay=zmax_config.retry_delay,
        )
        self._buffer = []
        self._channel_names = [data_type.name for data_type in self.SETTINGS.data_types]

    def shutdown(self):
        # TODO: handle data in buffer
        self._zmax.close()

    @ez.publisher(OUTPUT_DATA)
    async def collect(self) -> AsyncGenerator:
        while True:
            try:
                sample = self._zmax.read(self.SETTINGS.data_types)
            except TimeoutError as e:
                logger.error(
                    f"Reading from ZMax timed out, retrying in"
                    f" {self.SETTINGS.retry_delay} seconds: {e}"
                )
                sleep(self.SETTINGS.retry_delay)
                continue

            self._buffer.append(sample)

            if len(self._buffer) >= self.SETTINGS.buffer_size:
                yield (
                    self.OUTPUT_DATA,
                    Data(
                        np.array(self._buffer),
                        sample_rate=ZMAX_SAMPLE_RATE,
                        channel_names=self._channel_names,
                    ),
                )
                self._buffer = []
