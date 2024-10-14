import logging
from pathlib import Path

from slumber import settings
from slumber.utils.logger import setup_logging


def test_setup_logging_default_config():
    assert "logging" in settings, "Logging is not configured in settings"

    setup_logging()

    logger = logging.getLogger("slumber")
    assert logger.level != logging.NOTSET, "Logger level is set to NOTSET"
    assert not logger.disabled, "Logger is disabled"
    assert len(logger.handlers) > 0, "No handlers are set for the logger"

    for handler in logger.handlers:
        assert isinstance(
            handler, logging.Handler
        ), f"Handler {handler} is not an instance of logging.Handler"
        assert (
            handler.formatter is not None
        ), f"Handler {handler} does not have a formatter set"

        if isinstance(handler, logging.FileHandler):
            log_file_path = Path(handler.baseFilename)
            assert log_file_path.exists(), f"Log file {log_file_path} does not exist"
