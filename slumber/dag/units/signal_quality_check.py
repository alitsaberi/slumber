import logging
from collections.abc import AsyncGenerator

import ezmsg.core as ez

from slumber.tasks.evaluate_signal_quality import evaluate_signal_quality
from slumber.utils.data import Data

logger = logging.getLogger("slumber")


class SignalQualityCheck(ez.Unit):
    DATA = ez.InputStream(Data)

    @ez.subscriber(DATA)
    async def check(self, data: Data) -> AsyncGenerator:
        acceptable = evaluate_signal_quality(
            data.array[:, :2], data.sample_rate
        )  # Only use the first two channels (EEG_LEFT and EEG_RIGHT)
        logger.info(f"Signal quality: {'good' if acceptable else 'bad'}")
