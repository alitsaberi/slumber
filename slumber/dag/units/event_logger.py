from collections.abc import AsyncGenerator
from datetime import datetime
from enum import Enum
from pathlib import Path

import ezmsg.core as ez
from ezmsg.util.messagelogger import MessageLogger
from pydantic import BaseModel, ConfigDict, Field

from slumber.dag.utils import PydanticSettings


class Event(BaseModel):
    type: Enum
    timestamp: datetime = Field(default_factory=datetime.now)
    duration: float = 0.0

    model_config = ConfigDict(extra="allow")


class Settings(PydanticSettings):
    output: Path | None = None


class EventLogger(MessageLogger):
    
    SETTINGS = Settings
    
    INPUT_MESSAGE = ez.InputStream(Event)
    OUTPUT_MESSAGE = ez.OutputStream(Event)

    @ez.subscriber(INPUT_MESSAGE)
    @ez.publisher(OUTPUT_MESSAGE)
    async def on_message(self, message: Event) -> AsyncGenerator:
        event_str = message.model_dump_json(exclude_none=True)
        for output_f in self.STATE.output_files.values():
            output_f.write(f"{event_str}\n")
            output_f.flush()
        yield (self.OUTPUT_MESSAGE, message)
