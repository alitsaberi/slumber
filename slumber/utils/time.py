from datetime import datetime
from typing_extensions import Literal

import pytz

from slumber import settings


def timestamp_to_datetime(
    timestamp: float, tz: str = settings["time_zone"]
) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone(tz))


def now(time_zone: str = settings["time_zone"]) -> datetime:
    return datetime.now(tz=pytz.timezone(time_zone))


def datetime_to_str(
    dt: datetime,
    time_spec: Literal[
        "auto", "hours", "minutes", "seconds", "microseconds"
    ] = "microseconds",
) -> str:
    return dt.isoformat(timespec=time_spec)