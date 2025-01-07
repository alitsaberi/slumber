import asyncio
import time
from collections import deque
from collections.abc import AsyncGenerator
from functools import cached_property
from typing import Annotated

import ezmsg.core as ez
import numpy as np
from ezmsg.util.rate import Rate
from loguru import logger
from pydantic import AfterValidator, ConfigDict

from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import SAMPLE_RATE as ZMAX_SAMPLE_RATE
from slumber.sources.zmax import DataType, ZMax, is_connected
from slumber.utils.data import Data, Sample
from slumber.utils.helpers import enum_by_name_validator


class Settings(PydanticSettings):
    zmax: Annotated[ZMax, AfterValidator(is_connected)]
    data_types: list[Annotated[DataType, enum_by_name_validator(DataType)]]
    buffer_duration: int = 10  # seconds
    retry_delay: int = 5  # seconds

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def channel_names(self) -> list[str]:
        return [data_type.name for data_type in self.data_types]

    @property
    def buffer_size(self) -> int:
        return self.buffer_duration * ZMAX_SAMPLE_RATE


class State(ez.State):
    buffer: deque
    publish_rate: Rate


class ZMaxDataReceiver(ez.Unit):
    SETTINGS = Settings
    STATE = State
    OUTPUT_SAMPLE = ez.OutputStream(Sample)

    def initialize(self) -> None:
        self.STATE.buffer = deque(maxlen=self.SETTINGS.buffer_size * 2)
        self.STATE.publish_rate = Rate(1 / self.SETTINGS.buffer_duration)

    @ez.publisher(OUTPUT_SAMPLE)
    async def receive(self) -> AsyncGenerator:
        while True:
            try:
                array = self.SETTINGS.zmax.read(self.SETTINGS.data_types)
                timestamp = time.time()
                self.STATE.buffer.append((timestamp, array))
            except TimeoutError:
                logger.warning(
                    "Timed out while waiting for data from ZMax."
                    f"Retrying in {self.SETTINGS.retry_delay} seconds..."
                )
                await asyncio.sleep(self.SETTINGS.retry_delay)
            except ConnectionError as e:
                logger.error(f"Error connecting to ZMax: {e}. Retrying to connect...")
                self.SETTINGS.zmax.connect()

    @ez.publisher(OUTPUT_SAMPLE)
    async def publish(self):
        while True:
            current_time = time.time()
            expected_buffer_end_time = (
                self.STATE.publish_rate.last_time + self.SETTINGS.buffer_duration
            )

            if expected_buffer_end_time < current_time:
                logger.warning(
                    f"Buffer is too old. Expected end time: {expected_buffer_end_time},"
                    f" current time: {current_time}"
                )

            await self.STATE.publish_rate.sleep()
            yield (self.OUTPUT_DATA, self._process_buffer())

    def _process_buffer(self) -> Data:
        current_time = time.time()
        current_array = np.array(self.STATE.buffer)

        if len(current_array) == 0:
            logger.warning("Buffer is empty. Returning empty data.")
            return Data(
                np.zeros((self.SETTINGS.buffer_size, len(self.SETTINGS.channel_names))),
                sample_rate=ZMAX_SAMPLE_RATE,
                channel_names=self.SETTINGS.channel_names,
            )

        timestamps = current_array[:, 0]
        samples = current_array[:, 1]

        # Get samples only from past duration
        duration_start = current_time - self.SETTINGS.buffer_duration
        mask = timestamps >= duration_start
        timestamps = timestamps[mask]
        samples = samples[mask]

        if np.any(~mask):
            logger.warning(
                f"Found {np.sum(~mask)} samples older than"
                f" {self.SETTINGS.buffer_duration} seconds."
            )

        regular_timestamps = np.linspace(
            duration_start,
            current_time,
            self.SETTINGS.buffer_size,
        )

        interpolated_samples = np.interp(regular_timestamps, timestamps, samples)

        return Data(
            interpolated_samples,
            sample_rate=ZMAX_SAMPLE_RATE,
            channel_names=self.SETTINGS.channel_names,
        )
