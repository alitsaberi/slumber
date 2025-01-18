import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Generic, TypeVar

import ezmsg.core as ez
import numpy as np
from ezmsg.util.rate import Rate
from loguru import logger
from pydantic import Field, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import (
    Data,
    Sample,
    TimestampedArray,
    samples_to_timestamped_array,
)

T = TypeVar("T")


class QueueSettings(PydanticSettings):
    max_size: int = Field(gt=0)
    leaky: bool = False
    log_queue_size_interval: float | None = Field(None, gt=0)


class CountQueueSettings(QueueSettings):
    publish_count: int = Field(1000, gt=0)

    @model_validator(mode="after")
    def check_publish_count(self) -> "CountQueueSettings":
        if self.publish_count > self.max_size:
            raise ValueError(
                f"publish_count ({self.publish_count}) must be"
                f" less than or equal to max_size ({self.max_size})."
            )
        return self


class TimeQueueSettings(QueueSettings):
    publish_interval: float = Field(gt=0)
    sample_rate: int = Field(ge=1)
    gap_threshold: float = Field(ge=0)
    channel_names: list[str] = Field(
        min_length=1
    )  # TODO: this should not be set manually
    dropped_samples_warn_threshold: int | None = Field(None, ge=0)
    timestamp_margin: float = Field(ge=0)  # TODO: add validation

    @property
    def expected_publish_samples(self) -> int:
        return int(self.publish_interval * self.sample_rate)


class QueueState(ez.State):
    queue: asyncio.Queue
    leaky: bool


class TimeQueueState(QueueState):
    publish_rate: Rate


class Queue(ez.Unit, Generic[T]):
    SETTINGS = QueueSettings
    STATE = QueueState

    INPUT = ez.InputStream(T)

    async def initialize(self):
        self.STATE.leaky = self.SETTINGS.leaky
        self.STATE.queue = asyncio.Queue(self.SETTINGS.max_size)

    @ez.task
    async def monitor_queue_size(self) -> None:
        if self.SETTINGS.log_queue_size_interval is None:
            return

        while True:
            await asyncio.sleep(self.SETTINGS.log_queue_size_interval)
            logger.debug(
                f"{self.address} has {self.STATE.queue.qsize()} samples queued."
            )

    @ez.subscriber(INPUT)
    async def on_message(self, message: T) -> None:
        if not self.STATE.leaky:
            await self.STATE.queue.put(message)
        else:
            try:
                self.STATE.queue.put_nowait(message)
            except asyncio.QueueFull:
                logger.warning(f"{self.address} queue is full, dropping sample.")
                self.STATE.queue.get_nowait()
                self.STATE.queue.put_nowait(message)


class CountQueue(Queue[Sample]):
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

            array = samples_to_timestamped_array(samples)
            logger.debug(f"{self.address} publishing {array}.")

            yield (self.OUTPUT, array)


# TODO: make a base TimeQueue thst doesn't regularize sample rate


class TimeQueue(Queue[Sample]):
    SETTINGS = TimeQueueSettings
    STATE = TimeQueueState

    OUTPUT = ez.OutputStream(TimestampedArray)

    async def initialize(self):
        await super().initialize()
        self.STATE.publish_rate = Rate(1 / self.SETTINGS.publish_interval)

    @ez.publisher(OUTPUT)
    async def publish(self) -> AsyncGenerator:
        while True:
            current_time = time.time()
            expected_publish_time = (
                self.STATE.publish_rate.last_time + self.SETTINGS.publish_interval
            )

            if expected_publish_time < current_time:
                # TODO: Handle the data in the gap
                logger.warning(
                    f"{self.address} is behind schedule by"
                    f" {current_time - expected_publish_time} seconds.",
                    extra={
                        "current_time": current_time,
                        "expected_publish_time": expected_publish_time,
                    },
                )

            await self.STATE.publish_rate.sleep()

            current_time = self.STATE.publish_rate.last_time
            cutoff_time = current_time - self.SETTINGS.publish_interval

            data = self._process_queue(start_time=cutoff_time, end_time=current_time)

            logger.debug(f"{self.address} publishing {data}.")
            yield (self.OUTPUT, data)

    def _process_queue(self, start_time: float, end_time: float) -> list[Sample]:
        regular_timestamps = np.linspace(
            start_time, end_time, self.SETTINGS.expected_publish_samples
        )
        array = np.zeros(
            (
                self.SETTINGS.expected_publish_samples,
                len(self.SETTINGS.channel_names),
            )
        )

        dropped_samples = 0
        index = 0
        while (
            not self.STATE.queue.empty()
            and index < self.SETTINGS.expected_publish_samples
        ):
            sample: Sample = self.STATE.queue.get_nowait()

            if sample.timestamp < start_time - self.SETTINGS.timestamp_margin:
                logger.warning(
                    "Dropping sample that is too old."
                    f" Cutoff time is {start_time} but"
                    f" sample timestamp is {sample.timestamp}"
                )
                dropped_samples += 1
                continue

            if (
                gap := sample.timestamp - regular_timestamps[index]
            ) > self.SETTINGS.gap_threshold:
                logger.debug(
                    f"Large gap ({gap} sec) detected in data."
                    f"Current index: {index}. Finding next closest index ...",
                    sample_timestamp=sample.timestamp,
                    index_timestamp=regular_timestamps[index],
                    gap_threshold=self.SETTINGS.gap_threshold,
                )
                index = np.argmin(np.abs(regular_timestamps[index:] - sample.timestamp))
                logger.debug(f"Found next closest index: {index}.")

            array[index, :] = sample.array
            index += 1

            if sample.timestamp >= end_time + self.SETTINGS.timestamp_margin:
                logger.debug(
                    f"Sample timestamp ({sample.timestamp}) is past"
                    f" end time + margin ({end_time + self.SETTINGS.timestamp_margin})."
                    " Stopping."
                )
                break

        if (
            self.SETTINGS.dropped_samples_warn_threshold is not None
            and dropped_samples > self.SETTINGS.dropped_samples_warn_threshold
        ):
            logger.warning(
                f"{self.address} dropped {dropped_samples} samples due to being too old"
            )

        return Data(
            array=array,
            timestamps=regular_timestamps,
            sample_rate=self.SETTINGS.sample_rate,
            channel_names=self.SETTINGS.channel_names,
        )
