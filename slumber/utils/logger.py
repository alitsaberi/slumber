import logging.config
import sys
from enum import Enum
from pathlib import Path
from typing import Any

from loguru import logger

from slumber import settings

_FILE_NAME_KEY = "file_name"


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


def setup_logging(log_dir: Path, config: dict[str, Any]) -> None:
    logger.remove()

    for handler_name, handler_config in config.items():
        handler_type = HandlerType(handler_name)

        sink = (
            log_dir / handler_config.pop(_FILE_NAME_KEY)
            if handler_type == HandlerType.FILE
            else sys.stdout
        )
        logger.add(sink, **handler_config)

    # # Intercept standard library logging
    # # This way, all logs from the root logger and other libraries using standard
    # # logging will be properly formatted and handled by Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


if __name__ == "__main__":
    log_dir = Path(settings["data_dir"])
    setup_logging(log_dir, settings["logging"])
    logger.info("Hello, World!")
