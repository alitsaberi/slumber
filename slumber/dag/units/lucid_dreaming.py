import asyncio
import time
from collections.abc import AsyncGenerator

import ezmsg.core as ez

from slumber.dag.utils import PydanticSettings


class Settings(PydanticSettings):
    pass


class State(ez.State):
    start_time: float


class Master(ez.Unit):
    SETTINGS = Settings
    STATE = State
    
    CUEING_ENABLE_SIGNAL = ez.OutputStream(bool)
    CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)
    CUEING_DECREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)

    async def initialize(self) -> None:
        self.STATE.start_time = time.time()

    async def shutdown(self) -> None:
        pass

    @ez.publisher(CUEING_ENABLE_SIGNAL)
    @ez.publisher(CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    @ez.publisher(CUEING_DECREASE_INTENSITY_SIGNAL)
    async def run(self) -> AsyncGenerator:
        await asyncio.sleep(5)
        yield (self.CUEING_ENABLE_SIGNAL, True)
        await asyncio.sleep(20)
        for _ in range(3):
            yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, True)
            await asyncio.sleep(20)
        yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)
        await asyncio.sleep(20)
        yield (self.CUEING_DECREASE_INTENSITY_SIGNAL, True)
        await asyncio.sleep(20)
        yield (self.CUEING_ENABLE_SIGNAL, False)
        await asyncio.sleep(20)
        raise ez.NormalTermination
        