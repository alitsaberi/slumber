from datetime import datetime
from typing import Literal

import pytz

from slumber import settings

DEFAULT_TIME_SEPARATOR = ":"


def timestamp_to_datetime(
    timestamp: float, tz: str = settings["time_zone"]
) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone(tz))


def now(time_zone: str = settings["time_zone"]) -> datetime:
    time_zone = pytz.timezone(time_zone) if time_zone else None
    return datetime.now(tz=time_zone)


def datetime_to_str(
    dt: datetime,
    time_spec: Literal[
        "auto", "hours", "minutes", "seconds", "microseconds"
    ] = "microseconds",
    time_separator: str = DEFAULT_TIME_SEPARATOR,
) -> str:
    return dt.isoformat(timespec=time_spec).replace(
        DEFAULT_TIME_SEPARATOR, time_separator
    )
