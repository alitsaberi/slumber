from dataclasses import dataclass
from datetime import timedelta

import numpy as np


@dataclass
class Data:
    array: np.ndarray
    sample_rate: int

    # TODO: validate that array is 2D

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
    def duration(self) -> int:
        """Returns the duration of data in timedelta format"""
        return timedelta(seconds=self.length / self.sample_rate)

    def get_all_periods_by_period_length(
        self, period_length: int, channel_indices: list[int] | None = None
    ) -> np.ndarray:
        """
        Returns all periods in data.
        Args:
            period_length (int): The length of each period in seconds.
            channel_indices (list[int]): A list of channel indices to return.
        Returns:
            np.ndarray: An numpy array.
                        Shape (n_periods, n_samples_per_period, n_channels)
        """
        n_samples_per_period = period_length * self.sample_rate
        return self.get_all_periods(n_samples_per_period, channel_indices)

    def get_all_periods(
        self, n_samples_per_period: int, channel_indices: list[int] | None = None
    ) -> np.ndarray:
        """
        Returns all periods in data.
        Args:
            n_samples_per_period (int): The number of samples in each period.
            channel_indices (list[int]): A list of channel indices to return.
        Returns:
            np.ndarray: An numpy array.
                        Shape (n_periods, n_samples_per_period, n_channels)
        """
        return self.get_periods_by_index(0, n_samples_per_period, channel_indices)

    def get_periods_by_index(
        self,
        start_index: int,
        n_samples_per_period: int,
        n_periods: int | None = None,
        channel_indices: list[int] | None = None,
    ) -> np.ndarray:
        """
        Returns a number of periods in data starting from a given index.

        Args:
            start_index (int): The index of the first period to return.
            n_samples_per_period (int): The number of samples in each period.
            n_periods (int): The number of periods to return. If None,
                             all periods from the start index to the end of
                             the data are returned.
            channel_indices (list[int]): A list of channel indices to return.

        Returns:
            np.ndarray: An numpy array
                        Shape: (n_periods, n_samples_per_period, n_channels)

        Raises:
            ValueError: If the requested number of periods exceeds
                        the length of the data.
        """

        if start_index < 0 or start_index >= self.length // n_samples_per_period:
            raise ValueError(f"Invalid start_index: {start_index}")

        if n_samples_per_period <= 0 or n_samples_per_period > self.length:
            raise ValueError(f"Invalid n_samples_per_period: {n_samples_per_period}")

        start_sample_index = start_index * n_samples_per_period
        n_available_samples = self.length - start_sample_index

        if n_periods is None:
            if self.length % n_samples_per_period != 0:
                raise ValueError(
                    f"Data length {self.length} is not a multiple of"
                    f" {n_samples_per_period}."
                )
            n_periods = n_available_samples // n_samples_per_period

        end_sample_index = start_sample_index + (n_samples_per_period * n_periods)

        if end_sample_index > self.length:
            raise ValueError(
                f"Requested {n_periods} periods, but only"
                f" {n_available_samples // n_samples_per_period}"
                " periods are available."
            )

        data = self.array[start_sample_index:end_sample_index, :]

        if channel_indices is not None:
            data = data[:, channel_indices]

        return data.reshape(n_periods, n_samples_per_period, -1)
