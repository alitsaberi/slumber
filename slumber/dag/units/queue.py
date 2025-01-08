import asyncio
import time
from collections.abc import AsyncGenerator

import ezmsg.core as ez
import numpy as np
from ezmsg.util.rate import Rate
from loguru import logger
from pydantic import Field

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import (
    Data,
    Sample,
    TimestampedArray,
    samples_to_timestamped_array,
)


class QueueSettings(PydanticSettings):
    max_size: int = Field(gte=0)
    publish_interval: int = Field(gt=0)
    leaky: bool = False
    log_queue_size_interval: float | None = None


class CountQueueSettings(QueueSettings):
    publish_count: int = Field(1000, gt=0)


class TimeQueueSettings(QueueSettings):
    output_sample_rate: int | None = None
    interpolate_missing: bool = False


class QueueState(ez.State):
    queue: asyncio.Queue
    leaky: bool
    publish_rate: Rate


class Queue(ez.Unit):
    SETTINGS = QueueSettings
    STATE = QueueState

    INPUT = ez.InputStream(Sample)

    async def initialize(self):
        self.STATE.leaky = self.SETTINGS.leaky
        self.STATE.queue = asyncio.Queue(self.SETTINGS.max_size)
        self.STATE.publish_rate = Rate(1 / self.SETTINGS.publish_interval)

    @ez.task
    async def monitor_queue_size(self) -> None:
        if self.SETTINGS.log_queue_size_interval is None:
            return

        while True:
            await asyncio.sleep(self.SETTINGS.log_queue_size_interval)
            logger.info(
                f"{self.address} has {self.STATE.queue.qsize()} samples queued."
            )

    @ez.subscriber(INPUT)
    async def on_sample(self, sample: Sample) -> None:
        if not self.STATE.leaky:
            await self.STATE.queue.put(sample)
        else:
            try:
                self.STATE.queue.put_nowait(sample)
            except asyncio.QueueFull:
                logger.warning(f"{self.address} queue is full, dropping sample.")
                self.STATE.queue.get_nowait()
                self.STATE.queue.put_nowait(sample)


class CountQueue(Queue):
    SETTINGS = CountQueueSettings
    STATE = QueueState

    OUTPUT = ez.OutputStream(TimestampedArray)

    @ez.publisher(OUTPUT)
    async def publish(self) -> AsyncGenerator:
        while True:
            samples = []
            for _ in range(self.SETTINGS.publish_count):
                sample = await self.STATE.queue.get()
                samples.append(sample)

            yield (self.OUTPUT, samples_to_timestamped_array(samples))
            await self.STATE.publish_rate.sleep()


class TimeQueue(Queue):
    SETTINGS = TimeQueueSettings
    STATE = QueueState

    OUTPUT = ez.OutputStream(TimestampedArray)

    @ez.publisher(OUTPUT)
    async def publish(self) -> AsyncGenerator:
        while True:
            current_time = time.time()
            expected_publish_time = (
                self.STATE.publish_rate.last_time + self.SETTINGS.publish_interval
            )

            if expected_publish_time < current_time:
                logger.warning(
                    f"{self.address} is behind schedule by"
                    f" {current_time - expected_publish_time} seconds."
                )

            await self.STATE.publish_rate.sleep()

            current_time = time.time()
            cutoff_time = current_time - self.SETTINGS.publish_interval

            data = self._process_queue(start_time=cutoff_time, end_time=current_time)

            if data is None:
                continue

            if self.SETTINGS.output_sample_rate is not None:
                data = self._regularize_sample_rate(
                    data, start_time=cutoff_time, end_time=current_time
                )

            logger.debug(f"{self.address} publishing {data}.")
            yield (self.OUTPUT, data)

    def _process_queue(
        self, start_time: float, end_time: float
    ) -> TimestampedArray | None:
        samples = []
        while not self.STATE.queue.empty():
            sample = self.STATE.queue.get_nowait()
            if sample.timestamp < start_time:
                logger.warning(
                    "Dropping sample that is too old."
                    f" Cutoff time is {start_time} but"
                    f" sample timestamp is {sample.timestamp}"
                )
                continue
            if sample.timestamp > end_time:
                logger.debug(
                    f"Sample timestamp {sample.timestamp} is in the future."
                    f" Current time is {end_time}."
                )
                self.STATE.queue.put_nowait(sample)
                break
            samples.append(sample)

        if not samples:
            logger.warning(f"No samples in queue for time {end_time}.")
            return

        return samples_to_timestamped_array(samples)

    def _regularize_sample_rate(
        self, data: TimestampedArray, start_time: float, end_time: float
    ) -> Data:
        regular_timestamps = np.linspace(
            start_time,
            end_time,
            self.SETTINGS.publish_interval * self.SETTINGS.output_sample_rate,
        )

        if self.SETTINGS.interpolate_missing:
            array = np.interp(regular_timestamps, data.timestamps, data.array)
        else:
            array = np.zeros((len(regular_timestamps), data.n_channels))
            indices = np.searchsorted(regular_timestamps, data.timestamps)
            array[indices] = data.array

        return Data(
            array=array,
            timestamps=regular_timestamps,
            sample_rate=self.SETTINGS.output_sample_rate,
            channel_names=data.channel_names,
        )
