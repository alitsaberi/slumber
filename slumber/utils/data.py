from dataclasses import dataclass
from datetime import timedelta

import numpy as np


@dataclass
class Data:
    array: (
        np.ndarray
    )  # TODO: if this attribute is reassigned, channel_names must be updated
    sample_rate: int
    channel_names: list[str] | None = None

    def __post_init__(self):
        if len(self.shape) != 2:
            raise ValueError(f"Data must be 2D, got {len(self.shape)}D")

        if self.channel_names is None:
            self.channel_names = [f"channel_{i}" for i in range(self.n_channels)]

        if len(self.channel_names) != self.n_channels:
            raise ValueError(
                f"Number of channel names ({len(self.channel_names)})"
                f" must match number of channels ({self.n_channels})."
            )

    def __str__(self) -> str:
        return (
            f"Data(shape={self.shape},"
            f" sample_rate={self.sample_rate},"
            f" channel_names={self.channel_names})"
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

    @property
    def duration(self) -> timedelta:
        """Returns the duration of data in timedelta format"""
        return timedelta(seconds=self.length / self.sample_rate)

    @property
    def index(self) -> np.ndarray:
        """Returns time points in seconds"""
        return np.arange(self.length) / self.sample_rate

    def __getitem__(
        self, key: slice | tuple[slice, int | str | list[int] | list[str]]
    ) -> "Data":
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
            # Handle channel name-based assignment
            channel_indices = [
                self.channel_names.index(c)
                for c in ([channels] if isinstance(channels, str) else channels)
            ]
            self.array[samples, channel_indices] = value
        else:
            # Handle numeric index-based assignment
            self.array[samples, channels] = value

    def loc(
        self, samples: slice | None = None, channels: str | list[str] | None = None
    ) -> "Data":
        if channels is None:
            channels = self.channel_names
        if isinstance(channels, str):
            channels = [channels]
        channel_indices = [self.channel_names.index(name) for name in channels]
        return self._slice_data(samples, channel_indices, channels)

    def iloc(
        self, samples: slice | None = None, channels: int | list[int] | None = None
    ) -> "Data":
        if channels is None:
            channels = list(range(self.n_channels))
        if isinstance(channels, int):
            channels = [channels]
        channel_names = [self.channel_names[i] for i in channels]
        return self._slice_data(samples, channels, channel_names)

    def slice_by_time(
        self,
        start_time: float = 0.0,
        end_time: float | None = None,
        channels: list[str] | None = None,
    ) -> "Data":
        """
        Slice the data by time in seconds.

        Args:
            start_time (float): Start time in seconds
            end_time (float | None): End time in seconds. If None, slices until the end
            channels (list[str] | None): List of channel names to slice. If None,
                                         slices all channels

        Returns:
            Data: A new Data object containing the sliced data
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate) if end_time is not None else None

        return self[start_sample:end_sample, channels]

    def _slice_data(
        self, samples: slice | None, channels: list, channel_names: list[str]
    ) -> "Data":
        samples = samples or slice(None)
        return Data(
            array=self.array[samples, channels],
            sample_rate=self.sample_rate,
            channel_names=channel_names,
        )

    def roll(self, shift: int) -> None:
        """Roll the data array by shift samples"""
        self.array = np.roll(self.array, shift)


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
