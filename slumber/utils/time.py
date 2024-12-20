from datetime import datetime
from typing import Literal

import pytz

from slumber import settings

DEFAULT_TIME_SEPARATOR = ":"
FILENAME_COMPATIBLE_TIME_SEPARATOR = "-"


def timestamp_to_datetime(
    timestamp: float, time_zone: str | None = settings["time_zone"]
) -> datetime:
    time_zone = pytz.timezone(time_zone) if time_zone else None
    return datetime.fromtimestamp(timestamp, tz=time_zone)


def now(time_zone: str | None = settings["time_zone"]) -> datetime:
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


def create_timestamped_name(
    prefix: str,
    extension: str | None = None,
    time_zone: str | None = None,
    time_spec: Literal[
        "auto", "hours", "minutes", "seconds", "microseconds"
    ] = "seconds",
) -> str:
    """
    Creates a name with timestamp using the format:
        prefix_YYYY-MM-DD_HH-MM-SS[.extension]

    Args:
        prefix: Prefix for the name
        extension: Optional file extension (without the dot).
        time_zone: Timezone to use for timestamp
            (defaults to None, so timezone information is not included)

    Returns:
        str: Formatted name with timestamp, optionally with extension
    """
    timestamp = datetime_to_str(
        now(time_zone=time_zone),
        time_spec=time_spec,
        time_separator=FILENAME_COMPATIBLE_TIME_SEPARATOR,
    )
    base_name = f"{prefix}_{timestamp}"
    return f"{base_name}.{extension}" if extension else base_name
