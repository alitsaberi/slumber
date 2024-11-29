import os

from loguru import logger

from slumber import settings
from slumber.utils.logger import (
    setup_logging,
)


def test_setup_logging_default_config(tmpdir):
    assert "logging" in settings, "Logging is not configured in settings"

    logging_config = settings["logging"]

    setup_logging(tmpdir, logging_config)

    print(logger._core.handlers)

    handler_names = [handler._name for handler in logger._core.handlers.values()]

    assert (
        f"'{os.path.join(tmpdir, 'slumber.log')}'" in handler_names
    ), "File handler is not configured"
