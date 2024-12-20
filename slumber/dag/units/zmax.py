import asyncio
import time
from collections.abc import AsyncGenerator
from functools import cached_property
from typing import Annotated

import ezmsg.core as ez
from loguru import logger
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    IPvAnyAddress,
)

from slumber.dag.utils import PydanticSettings
from slumber.sources.zmax import (
    DEFAULTS,
    LED_MAX_INTENSITY,
    LED_MIN_INTENSITY,
    STIMULATION_MAX_DURATION,
    STIMULATION_MAX_REPETITIONS,
    STIMULATION_MIN_DURATION,
    STIMULATION_MIN_REPETITIONS,
    ConnectionClosedError,
    DataType,
    LEDColor,
    ZMax,
)
from slumber.utils.data import Sample
from slumber.utils.helpers import create_enum_by_name_resolver


class ZMaxStimulationSignal(BaseModel):
    vibration: bool
    led_color: Annotated[
        LEDColor, BeforeValidator(create_enum_by_name_resolver(LEDColor))
    ]
    on_duration: int = Field(ge=STIMULATION_MIN_DURATION, le=STIMULATION_MAX_DURATION)
    off_duration: int = Field(ge=STIMULATION_MIN_DURATION, le=STIMULATION_MAX_DURATION)
    repetitions: int = Field(
        ge=STIMULATION_MIN_REPETITIONS, le=STIMULATION_MAX_REPETITIONS
    )
    led_intensity: int = Field(
        LED_MAX_INTENSITY,
        ge=LED_MIN_INTENSITY,
        le=LED_MAX_INTENSITY,
    )
    alternate_eyes: bool = False


class ZMaxConfig(BaseModel):
    ip: IPvAnyAddress = DEFAULTS["ip"]
    port: int = Field(DEFAULTS["port"], ge=0)
    socket_timeout: float | None = Field(
        DEFAULTS["socket_timeout"],
        description=(
            "Socket timeout in seconds."
            " If zero is given, the socket is put in non-blocking mode."
            " If None is given, the socket is put in blocking mode."
        ),
        ge=0,
    )


class Settings(PydanticSettings):
    zmax: ZMaxConfig
    data_types: set[
        Annotated[DataType, BeforeValidator(create_enum_by_name_resolver(DataType))]
    ] = Field(set(list(DataType)), min_length=1)
    retry_attempts: int | None = Field(DEFAULTS["retry_attempts"], ge=0)
    retry_delay: float = Field(DEFAULTS["retry_delay"], ge=0.0)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def channel_names(self) -> list[str]:
        return [data_type.name for data_type in self.data_types]


class State(ez.State):
    zmax: ZMax


class ZMaxDataReceiver(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT_STIMULATION_SIGNAL = ez.InputStream(ZMaxStimulationSignal)

    OUTPUT_SAMPLE = ez.OutputStream(Sample)

    async def initialize(self):
        self.STATE.zmax = ZMax(**self.SETTINGS.zmax.model_dump())
        self.STATE.zmax.connect(
            retry_attempts=self.SETTINGS.retry_attempts,
            retry_delay=self.SETTINGS.retry_delay,
        )

    async def shutdown(self) -> None:
        self.STATE.zmax.disconnect()

    @ez.main
    @ez.publisher(OUTPUT_SAMPLE)
    async def publish_sample(self) -> AsyncGenerator:
        while True:
            try:
                array = self.STATE.zmax.read(self.SETTINGS.data_types)
                yield (
                    self.OUTPUT_SAMPLE,
                    Sample(
                        array=array,
                        timestamp=time.time(),
                        channel_names=self.SETTINGS.channel_names,
                    ),
                )
            except TimeoutError:
                logger.warning(
                    "Timeout while reading from ZMax."
                    " Possible causes: Connection between ZMax and PC is lost"
                    " (e.g., ZMax is off or dongle is disconnected),"
                    " ZMax server is closed, or HDRecorder has never been connected."
                )
                await asyncio.sleep(self.SETTINGS.retry_delay)
                self.STATE.zmax.flush_buffer(
                    retry_attempts=self.SETTINGS.retry_attempts,
                    retry_delay=self.SETTINGS.retry_delay,
                )
            except ConnectionClosedError:
                logger.warning("ZMax server closed connection. Reconnecting...")
                self.STATE.zmax.flush_buffer(
                    retry_attempts=self.SETTINGS.retry_attempts,
                    retry_delay=self.SETTINGS.retry_delay,
                )

    @ez.subscriber(INPUT_STIMULATION_SIGNAL)
    async def stimulate(self, signal: ZMaxStimulationSignal) -> None:
        logger.debug(f"Stimulating {signal}")
        self.STATE.zmax.stimulate(**signal.model_dump())
