import sys

from loguru import logger

from slumber import settings
from slumber.utils.logger import (
    setup_logging,
)


def test_setup_logging_default_config(tmpdir):
    assert "logging" in settings, "Logging is not configured in settings"

    logging_config = settings["logging"]

    setup_logging(tmpdir, logging_config)
    assert (
        logger.handlers[0].sink == sys.stdout
    ), "First handler is not set to sys.stdout"
    assert (
        logger.handlers[1].sink.name == "slumber.log"
    ), "Second handler is not set to slumber.log"
