class SlumberError(Exception):
    """Base exception class for Slumber application"""

    pass


class TimeRangeError(SlumberError):
    """Raised when a time value is outside the acceptable range"""

    pass


class SessionNotFoundError(SlumberError):
    """Raised when a session is not found"""

    pass
