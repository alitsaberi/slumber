from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from loguru import logger

from slumber import settings

_FILE_NAME_KEY = "file_name"


_audit_logger = logger.bind(audit=True)
_audit_logger.remove()


class AuditType(Enum):
    APP_START = 1
    APP_SHUTDOWN = 2


@dataclass
class Event:
    type: AuditType
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = "-"
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type.name,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "extra": self.extra,
        }


def setup_audit(data_dir: Path, config: dict[str, Any]) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    sink = data_dir / config.pop(_FILE_NAME_KEY)
    config["message"] = "{message}"
    _audit_logger.add(sink, **config)


def log_event(event: Event) -> None:
    event_dict = event.to_dict()
    tsv_line = "\t".join([str(event_dict[key]) for key in event_dict])
    _audit_logger.info(tsv_line)


if __name__ == "__main__":
    data_dir = Path(settings["data_dir"])
    setup_audit(data_dir, settings["audit"])
    log_event(Event(AuditType.APP_START, description="Application started"))
    log_event(Event(AuditType.APP_SHUTDOWN, description="Application shutdown"))
