import asyncio
import time
from collections.abc import AsyncGenerator
from functools import cached_property
from typing import Annotated

import ezmsg.core as ez
from loguru import logger
from pydantic import AfterValidator, ConfigDict

from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import DataType, ZMax, is_connected
from slumber.utils.data import Sample
from slumber.utils.helpers import enum_by_name_validator


class Settings(PydanticSettings):
    zmax: Annotated[ZMax, AfterValidator(is_connected)] | None
    data_types: list[Annotated[DataType, enum_by_name_validator(DataType)]]
    retry_delay: int = 5  # seconds

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def channel_names(self) -> list[str]:
        return [data_type.name for data_type in self.data_types]


class ZMaxDataReceiver(ez.Unit):
    SETTINGS = Settings

    SAMPLE = ez.OutputStream(Sample)

    @ez.publisher(SAMPLE)
    async def publish_sample(self) -> AsyncGenerator:
        while True:
            try:
                array = self.SETTINGS.zmax.read(self.SETTINGS.data_types)
                yield (
                    self.SAMPLE,
                    Sample(
                        array=array,
                        timestamp=time.time(),
                        channel_names=self.SETTINGS.channel_names,
                    ),
                )
            except TimeoutError:
                logger.warning(
                    "Timed out while waiting for data from ZMax."
                    f"Retrying in {self.SETTINGS.retry_delay} seconds..."
                )
                await asyncio.sleep(self.SETTINGS.retry_delay)
            except ConnectionError as e:
                logger.error(f"Error connecting to ZMax: {e}. Retrying to connect...")
                self.SETTINGS.zmax.connect()
