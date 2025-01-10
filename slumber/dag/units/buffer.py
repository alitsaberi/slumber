from collections.abc import AsyncGenerator

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import Field

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import Data, TimestampedArray


class RollingBufferSettings(PydanticSettings):
    size: int = Field(gt=0)


class RollingBufferState(ez.State):
    buffer: TimestampedArray | None = None
    data_length: int = None


class RollingBuffer(ez.Unit):
    SETTINGS = RollingBufferSettings
    STATE = RollingBufferState

    INPUT = ez.InputStream(Data)
    OUTPUT = ez.OutputStream(Data)

    @ez.subscriber(INPUT)
    @ez.publisher(OUTPUT)
    async def on_message(self, data: Data) -> AsyncGenerator:
        self._update_buffer(data)
        yield (self.OUTPUT, self.STATE.buffer)

    def _update_buffer(self, data: Data) -> None:
        if not isinstance(data, Data):
            raise TypeError(f"Input must be a Data instance but was {type(data)}")

        if self.STATE.buffer is None:
            self._initialize_buffer(data)

        if data.length != self.STATE.data_length:
            raise ValueError(
                f"Input length {data.length} does not match"
                f" expected length {self.STATE.data_length}"
            )

        self.STATE.buffer.roll(-data.length)
        self.STATE.buffer[-data.length :] = data

    def _initialize_buffer(self, data: Data) -> None:
        self.STATE.data_length = data.length
        self.STATE.buffer = Data(
            array=np.zeros(
                (
                    self.SETTINGS.size * data.length,
                    data.n_channels,
                )
            ),
            sample_rate=data.sample_rate,
            channel_names=data.channel_names,
            timestamp_offset=data.timestamps[0]
            - (data.length / data.sample_rate) * (self.SETTINGS.size - 1),
        )

        assert np.equal(
            self.STATE.buffer.timestamps[-data.length :], data.timestamps
        ).all()

        logger.info(f"Initialized rolling buffer: {self.STATE.buffer}")
