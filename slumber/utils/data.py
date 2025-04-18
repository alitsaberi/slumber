from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

from slumber.utils.time import timestamp_to_datetime


class NoSamplesError(ValueError): ...


def _validate_channel_names(objects: Sequence["ArrayBase"]) -> None:
    reference_channels = objects[0].channel_names
    for obj in objects[1:]:
        if obj.channel_names != reference_channels:
            raise ValueError(
                "All objects must have identical channel names."
                f" Reference: {reference_channels}, got: {obj.channel_names}"
            )
    return reference_channels


@dataclass
class ArrayBase:
    array: np.ndarray[Any, np.dtype[np.float64]]
    channel_names: list[str]

    def __post_init__(self):
        if not isinstance(self.array, np.ndarray):
            raise TypeError("array must be a numpy.ndarray")

        if self.channel_names is None:
            self.channel_names = [f"channel_{i}" for i in range(self.n_channels)]

        if len(self.channel_names) != self.n_channels:
            raise ValueError(
                f"Number of channel names ({len(self.channel_names)})"
                f" must match number of channels ({self.n_channels})."
            )

    # TODO: use dataclass methods for serialization
    def __str__(self) -> str:
        attrs = [f"{k}={v}" for k, v in self.attributes.items()]
        return f"{self.__class__.__name__}(shape={self.shape}, {', '.join(attrs)})"

    @property
    def attributes(self) -> dict[str, Any]:
        return {
            "channel_names": self.channel_names,
        }

    @property
    def datasets(self) -> dict[str, np.ndarray]:
        return {
            "data": self.array,
        }

    @property
    def shape(self) -> tuple[int, int]:
        """Returns the shape of data"""
        return self.array.shape

    @property
    def n_channels(self) -> int:
        """Returns the number of channels in data"""
        return self.array.shape[-1]

    @cached_property
    def channel_index_map(self) -> dict[str, int]:
        """Returns a mapping from channel name to index"""
        return {name: idx for idx, name in enumerate(self.channel_names)}

    def to_csv(self, path: Path) -> None:
        """Saves data to a CSV file"""

        if path.exists():
            logger.warning(f"File {path} already exists, overwriting")

        with open(path, "w") as f:
            f.write(",".join(self.channel_names) + "\n")
            for row in self.array:
                f.write(",".join(map(str, row)) + "\n")


@dataclass
class Sample(ArrayBase):
    timestamp: float
    # TODO: non-default argument 'timestamp' follows default argument

    def __post_init__(self):
        super().__post_init__()

        if self.array.ndim != 1:
            raise ValueError(
                f"Data must be 1D with shape (n_channels,), got shape {self.shape}"
            )

    @property
    def datasets(self) -> dict[str, np.ndarray]:
        return {
            "data": self.array.reshape(-1, 1),
            "timestamp": np.array([self.timestamp]),
        }


@dataclass
class TimestampedArray(ArrayBase):
    timestamps: np.ndarray[np.float64]

    @property
    def length(self) -> int:
        """Returns the number of samples in data"""
        return self.shape[0]

    @property
    def index(self) -> np.ndarray:
        """
        Return the time index of the data relative to the start time.
        """
        return self.timestamps - self.timestamps[0]

    @property
    def datasets(self) -> dict[str, np.ndarray]:
        return {
            "data": self.array,
            "timestamp": self.timestamps,
        }

    def __post_init__(self):
        super().__post_init__()

        if self.array.ndim != 2:
            raise ValueError(
                f"Data must be 2D with shape (n_samples, n_channels), "
                f"got shape {self.shape}"
            )

        if self.timestamps.shape != (self.length,):
            raise ValueError(
                f"Timestamps must have shape (n_samples,), "
                f"got shape {self.timestamps.shape}"
            )

    def __getitem__(
        self, key: slice | tuple[slice, int | str | list[int] | list[str]]
    ) -> "TimestampedArray":
        """Support for array-like slicing with [channel_names/indices]"""
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
        value: "TimestampedArray",
    ) -> None:
        """Support for array-like assignment with [start:stop, channel_names/indices]"""

        if not isinstance(value, self.__class__):
            raise TypeError(f"Assignment value must be a {self.__class__} instance.")

        if not isinstance(key, tuple):
            self.array[key] = value.array
            self.timestamps[key] = value.timestamps
            return

        samples, channels = key

        self.timestamps[samples] = value.timestamps

        if isinstance(channels, str):
            channels = [channels]

        if isinstance(channels, list) and all(isinstance(c, str) for c in channels):
            channel_indices = self.get_channel_indices(channels)
            self.array[samples, channel_indices] = value
        else:
            self.array[samples, channels] = value

    def loc(
        self, samples: slice | None = None, channels: str | list[str] | None = None
    ) -> "TimestampedArray":
        if channels is None:
            channels = self.channel_names

        if isinstance(channels, str):
            channels = [channels]

        channel_indices = self.get_channel_indices(channels)
        return self._slice_data(samples, channel_indices, channels)

    def iloc(
        self, samples: slice | None = None, channels: int | list[int] | None = None
    ) -> "TimestampedArray":
        if channels is None:
            channels = list(range(self.n_channels))
        if isinstance(channels, int):
            channels = [channels]
        channel_names = [self.channel_names[i] for i in channels]
        return self._slice_data(samples, channels, channel_names)

    def get_channel_indices(self, channels: list[str]) -> list[int]:
        return [self.channel_index_map[ch] for ch in channels]

    def _slice_data(
        self, samples: slice | None, channels: list, channel_names: list[str]
    ) -> "TimestampedArray":
        samples = samples or slice(None)
        kwargs = self._get_slice_kwargs(samples, channels, channel_names)
        return type(self)(**kwargs)

    def _get_slice_kwargs(
        self, samples: slice, channels: list[int], channel_names: list[str]
    ) -> dict[str, Any]:
        return {
            "array": self.array[samples, channels],
            "channel_names": channel_names,
            "timestamps": self.timestamps[samples],
        }

    def roll(self, shift: int) -> None:
        self.array = np.roll(self.array, shift, axis=0)
        self.timestamps = np.roll(self.timestamps, shift)

    @classmethod
    def concatenate(cls, objects: Sequence["TimestampedArray"]) -> "TimestampedArray":
        if len(objects) == 0:
            raise ValueError("At least one object must be provided.")

        channel_names = _validate_channel_names(objects)
        array = np.concatenate([obj.array for obj in objects], axis=0)
        timestamps = np.concatenate([obj.timestamps for obj in objects])
        return TimestampedArray(
            array=array, channel_names=channel_names, timestamps=timestamps
        )


@dataclass
class Data(TimestampedArray):
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
        timestamps = timestamps + timestamp_offset

        super().__init__(
            array=array,
            channel_names=channel_names,
            timestamps=timestamps,
        )

    def _get_slice_kwargs(
        self, samples: slice, channels: list, channel_names: list[str]
    ) -> dict[str, Any]:
        kwargs = super()._get_slice_kwargs(samples, channels, channel_names)
        kwargs["sample_rate"] = self.sample_rate
        return kwargs

    def __setitem__(
        self,
        key: slice | tuple[slice, int | str | list[int] | list[str]],
        value: "Data",
    ) -> None:
        if value.sample_rate != self.sample_rate:
            raise ValueError(
                f"Sample rate mismatch: {value.sample_rate} != {self.sample_rate}"
            )

        super().__setitem__(key, value)

    @property
    def index(self) -> np.ndarray:
        return np.arange(self.length, dtype=np.int32) / self.sample_rate

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.length / self.sample_rate)

    @property
    def attributes(self) -> dict[str, Any]:
        return {
            "sample_rate": self.sample_rate,
            **super().attributes,
        }

    @classmethod
    def concatenate(
        cls,
        objects: Sequence["Data"],
    ) -> "Data":
        base = super().concatenate(objects)

        sample_rate = objects[0].sample_rate
        if not all(obj.sample_rate == sample_rate for obj in objects):
            raise ValueError("All objects must have the same sample rate")

        return Data(
            array=base.array,
            channel_names=base.channel_names,
            timestamps=base.timestamps,
            sample_rate=sample_rate,
        )


def samples_to_timestamped_array(samples: Sequence[Sample]) -> TimestampedArray:
    if len(samples) == 0:
        raise NoSamplesError("No samples provided")

    channels_names = _validate_channel_names(samples)

    array = np.stack([sample.array for sample in samples])
    timestamps = np.array([sample.timestamp for sample in samples])

    return TimestampedArray(
        array=array,
        channel_names=channels_names,
        timestamps=timestamps,
    )


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
                f"Data length {data.length} is not"
                f" a multiple of {n_samples_per_period}."
            )
        n_periods = n_available_samples // n_samples_per_period

    end_sample_index = start_sample_index + (n_samples_per_period * n_periods)

    if end_sample_index > data.length:
        raise ValueError(
            f"Requested {n_periods} periods, but only"
            f" {n_available_samples // n_samples_per_period} periods are available."
        )

    period_indices = np.arange(start_sample_index, end_sample_index)
    period_indices = period_indices.reshape(n_periods, n_samples_per_period)

    return data.array[period_indices]


@dataclass
class Event:
    label: str
    start_time: float
    end_time: float

    def __repr__(self) -> str:
        return (
            f"Event(label={self.label},"
            f" start_time={timestamp_to_datetime(self.start_time)},"
            f" end_time={timestamp_to_datetime(self.end_time)})"
        )
