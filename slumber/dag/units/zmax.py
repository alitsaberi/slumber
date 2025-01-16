import time
from collections.abc import AsyncGenerator
from functools import cached_property
from typing import Annotated

import ezmsg.core as ez
from loguru import logger
from pydantic import AfterValidator, BeforeValidator, ConfigDict

from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import DataType, ZMax, is_connected
from slumber.utils.data import Sample
from slumber.utils.helpers import create_enum_by_name_resolver


class Settings(PydanticSettings):
    zmax: Annotated[ZMax, AfterValidator(is_connected)] | None
    data_types: list[
        Annotated[DataType, BeforeValidator(create_enum_by_name_resolver(DataType))]
    ]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def channel_names(self) -> list[str]:
        return [data_type.name for data_type in self.data_types]


class ZMaxDataReceiver(ez.Unit):
    SETTINGS = Settings

    SAMPLE = ez.OutputStream(Sample)

    async def initialize(self):
        self.SETTINGS.zmax.flush_buffer()

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
                logger.warning("Timed out while waiting for data from ZMax.")
            except ConnectionError as e:
                logger.warning(f"Error connecting to ZMax: {e}. Retrying to connect...")
                self.SETTINGS.zmax.connect()
