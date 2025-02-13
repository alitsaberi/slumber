import logging.config
import sys
from enum import Enum
from pathlib import Path
from typing import Any

from logtail import LogtailHandler
from loguru import logger

from slumber import settings


class HandlerType(Enum):
    CONSOLE = "console"
    FILE = "file"
    LOGTAIL = "logtail"


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_file: Path, config: dict[str, Any] = settings["logging"]) -> None:
    logger.remove()

    for handler_name, handler_config in config["handlers"].items():
        handler_type = HandlerType(handler_name)

        match handler_type:
            case HandlerType.CONSOLE:
                sink = sys.stdout
            case HandlerType.LOGTAIL:
                sink = LogtailHandler(
                    source_token=handler_config.pop("source_token"),
                    host=handler_config.pop("host"),
                )
            case HandlerType.FILE:
                sink = log_file

        logger.add(sink, **handler_config)

    # Intercept standard library logging
    # This way, all logs from the root logger and other libraries using standard
    # logging will be properly formatted and handled by Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
