import logging.config
import sys
from enum import Enum
from pathlib import Path
from typing import Any

from loguru import logger

from slumber import settings


class HandlerType(Enum):
    CONSOLE = "console"
    FILE = "file"


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

        sink = log_file if handler_type == HandlerType.FILE else sys.stdout
        logger.add(sink, **handler_config)

    # Intercept standard library logging
    # This way, all logs from the root logger and other libraries using standard
    # logging will be properly formatted and handled by Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
