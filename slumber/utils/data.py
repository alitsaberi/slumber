from dataclasses import dataclass
from datetime import timedelta
from typing import Any

import numpy as np


@dataclass
class ArrayBase:
    array: np.ndarray
    channel_names: list[str]

    def __post_init__(self):
        if len(self.shape) != 2:
            raise ValueError(
                f"Data must be 2D with shape (n_samples, n_channels), "
                f"got shape {self.shape}"
            )

        if self.channel_names is None:
            self.channel_names = [f"channel_{i}" for i in range(self.n_channels)]

        if len(self.channel_names) != self.n_channels:
            raise ValueError(
                f"Number of channel names ({len(self.channel_names)})"
                f" must match number of channels ({self.n_channels})."
            )

    @property
    def shape(self) -> tuple[int, int]:
        """Returns the shape of data"""
        return self.array.shape

    @property
    def length(self) -> int:
        """Returns the number of samples in data"""
        return self.shape[0]

    @property
    def n_channels(self) -> int:
        """Returns the number of channels in data"""
        return self.shape[1]

    def __getitem__(
        self, key: slice | tuple[slice, int | str | list[int] | list[str]]
    ) -> "ArrayBase":
        """Support for array-like slicing with [start:stop, channel_names/indices]"""
        if not isinstance(key, tuple):
            key = (key, None)
        samples, channels = key
        if isinstance(channels, str) or (
            isinstance(channels, list) and all(isinstance(c, str) for c in channels)
        ):
            return self.loc(samples, channels)
        return self.iloc(samples, channels)

    def __setitem__(
        self,
        key: slice | tuple[slice, int | str | list[int] | list[str]],
        value: float | np.ndarray,
    ) -> None:
        """Support for array-like assignment with [start:stop, channel_names/indices]"""
        if not isinstance(key, tuple):
            self.array[key] = value
            return

        samples, channels = key
        if isinstance(channels, str) or (
            isinstance(channels, list) and all(isinstance(c, str) for c in channels)
        ):
            channel_indices = [
                self.channel_names.index(c)
                for c in ([channels] if isinstance(channels, str) else channels)
            ]
            self.array[samples, channel_indices] = value
        else:
            self.array[samples, channels] = value

    def loc(
        self, samples: slice | None = None, channels: str | list[str] | None = None
    ) -> "ArrayBase":
        if channels is None:
            channels = self.channel_names
        if isinstance(channels, str):
            channels = [channels]
        channel_indices = [self.channel_names.index(name) for name in channels]
        return self._slice_data(samples, channel_indices, channels)

    def iloc(
        self, samples: slice | None = None, channels: int | list[int] | None = None
    ) -> "ArrayBase":
        if channels is None:
            channels = list(range(self.n_channels))
        if isinstance(channels, int):
            channels = [channels]
        channel_names = [self.channel_names[i] for i in channels]
        return self._slice_data(samples, channels, channel_names)

    def _slice_data(
        self, samples: slice | None, channels: list, channel_names: list[str]
    ) -> "ArrayBase":
        samples = samples or slice(None)
        kwargs = self._get_slice_kwargs(samples, channels, channel_names)
        return type(self)(**kwargs)

    def _get_slice_kwargs(
        self, samples: slice, channels: list, channel_names: list[str]
    ) -> dict[str, Any]:
        return {
            "array": self.array[samples, channels],
            "channel_names": channel_names,
        }

    def roll(self, shift: int) -> None:
        self.array = np.roll(self.array, shift)


@dataclass
class TimeSeriesBase(ArrayBase):
    timestamps: np.ndarray[float]

    def __post_init__(self):
        super().__post_init__()

        if self.timestamps.shape != (self.length,):
            raise ValueError(
                f"Timestamps must have shape (n_samples,), "
                f"got shape {self.timestamps.shape}"
            )

    @property
    def index(self) -> np.ndarray:
        """
        Return the time index of the data relative to the start time.
        """
        return self.timestamps - self.timestamps[0]

    def _get_slice_kwargs(
        self, samples: slice, channels: list, channel_names: list[str]
    ) -> dict[str, Any]:
        kwargs = super()._get_slice_kwargs(samples, channels, channel_names)
        kwargs["timestamps"] = self.timestamps[samples]
        return kwargs

    def roll(self, shift: int) -> None:
        super().roll(shift)
        self.timestamps = np.roll(self.timestamps, shift)


@dataclass
class Data(TimeSeriesBase):
    """
    Represents a time series of data with constant sample rate.
    """

    sample_rate: int

    def __init__(
        self,
        array: np.ndarray,
        sample_rate: int,
        channel_names: list[str] | None = None,
        timestamp_offset: float = 0.0,
        timestamps: np.ndarray | None = None,
    ) -> None:
        if sample_rate <= 0:
            raise ValueError(f"Sample rate must be positive, got {sample_rate}")

        self.array = array
        self.sample_rate = sample_rate
        timestamps = timestamps if timestamps is not None else self.index
        super().__init__(
            array=array,
            channel_names=channel_names,
            timestamps=timestamps + timestamp_offset,
        )

    def __str__(self):
        return (
            f"Data(shape={self.shape}, sample_rate={self.sample_rate},"
            f" channel_names={self.channel_names})"
        )

    def _get_slice_kwargs(
        self, samples: slice, channels: list, channel_names: list[str]
    ) -> dict[str, Any]:
        kwargs = super()._get_slice_kwargs(samples, channels, channel_names)
        kwargs["sample_rate"] = self.sample_rate
        return kwargs

    @property
    def index(self) -> np.ndarray:
        return np.arange(self.length, dtype=np.int32) / self.sample_rate

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.length / self.sample_rate)


def get_all_periods_by_period_length(
    data: Data,
    period_length: int,
) -> np.ndarray:
    """
    Returns all periods in data.
    Args:
        data (Data): The data to get periods from.
        period_length (int): The length of each period in seconds.
    Returns:
        np.ndarray: An numpy array.
                    Shape (n_periods, n_samples_per_period, n_channels)
    """
    n_samples_per_period = period_length * data.sample_rate
    return get_all_periods(data, n_samples_per_period)


def get_all_periods(data: Data, n_samples_per_period: int) -> np.ndarray:
    """
    Returns all periods in data.
    Args:
        data (Data): The data to get periods from.
        n_samples_per_period (int): The number of samples in each period.
    Returns:
        np.ndarray: An numpy array.
                    Shape (n_periods, n_samples_per_period, n_channels)
    """
    return get_periods_by_index(data, 0, n_samples_per_period, None)


def get_periods_by_index(
    data: Data,
    start_index: int,
    n_samples_per_period: int,
    n_periods: int | None = None,
) -> np.ndarray:
    """
    Returns a number of periods in data starting from a given index.

    Args:
        data (Data): The data to get periods from.
        start_index (int): The index of the first period to return.
        n_samples_per_period (int): The number of samples in each period.
        n_periods (int): The number of periods to return. If None,
                            all periods from the start index to the end of
                            the data are returned.

    Returns:
        np.ndarray: An numpy array
                    Shape: (n_periods, n_samples_per_period, n_channels)

    Raises:
        ValueError: If the requested number of periods exceeds
                    the length of the data.
    """
    if start_index < 0 or start_index >= data.length // n_samples_per_period:
        raise ValueError(f"Invalid start_index: {start_index}")

    if n_samples_per_period <= 0 or n_samples_per_period > data.length:
        raise ValueError(f"Invalid n_samples_per_period: {n_samples_per_period}")

    start_sample_index = start_index * n_samples_per_period
    n_available_samples = data.length - start_sample_index

    if n_periods is None:
        if data.length % n_samples_per_period != 0:
            raise ValueError(
                f"Data length {data.length} is not a multiple of"
                f" {n_samples_per_period}."
            )
        n_periods = n_available_samples // n_samples_per_period

    end_sample_index = start_sample_index + (n_samples_per_period * n_periods)

    if end_sample_index > data.length:
        raise ValueError(
            f"Requested {n_periods} periods, but only"
            f" {n_available_samples // n_samples_per_period}"
            " periods are available."
        )

    selected_data = data[start_sample_index:end_sample_index]

    return selected_data.array.reshape(n_periods, n_samples_per_period, -1)
