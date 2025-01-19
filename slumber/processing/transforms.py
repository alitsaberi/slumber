from typing import Literal, Protocol, runtime_checkable

import numpy as np
from mne.filter import filter_data, resample

from slumber.utils.data import Data, TimestampedArray


@runtime_checkable
class Transform(Protocol):
    def __call__(self, data: Data, **kwargs) -> Data:
        """
        Protocol for transform functions that process Data objects.

        Args:
            data (Data): Input data object containing array and sample rate
            **kwargs: Additional arguments specific to each transform implementation

        Returns:
            Data: Transformed data object
        """
        ...


class FIRFilter(Transform):
    def __call__(
        self,
        data: Data,
        low_cutoff: float | None = None,
        high_cutoff: float | None = None,
        **kwargs,
    ) -> Data:
        """
        Apply FIR filter with a Hamming window. The filter length is automatically
        chosen using the filter design function.

        Args:
            data (Data): Input data object containing array and sample rate.
            low_cutoff (float, optional): The lower frequency bound of
                the bandpass filter in Hz.
                If None, a highpass filter is applied. Default is None.
            high_cutoff (float, optional): The upper frequency bound of
                the bandpass filter in Hz.
                If None, a lowpass filter is applied. Default is None.

        Returns:
            Data: The filtered data.

        Notes:
            If both `low_cutoff` and `high_cutoff` are None,
            the original data is returned unchanged.
            If only `low_cutoff` is provided, a highpass filter is applied.
            If only `high_cutoff` is provided, a lowpass filter is applied.
            If `low_cutoff` is greater than `high_cutoff`, a bandstop filter is applied.
            If `low_cutoff` is less than `high_cutoff`, a bandpass filter is applied.
        """
        return Data(
            filter_data(
                data.array.T, data.sample_rate, low_cutoff, high_cutoff, **kwargs
            ).T,
            sample_rate=data.sample_rate,
            channel_names=data.channel_names,
            timestamps=data.timestamps,
        )


class Resample(Transform):
    def __call__(
        self,
        data: Data,
        new_sample_rate: int,
        method: Literal["fft", "polyphase"] = "polyphase",
        **kwargs,
    ) -> Data:
        return Data(
            resample(
                data.array.astype(np.float64),
                new_sample_rate,
                data.sample_rate,
                method=method,
                axis=0,
                **kwargs,
            ),
            sample_rate=new_sample_rate,
            channel_names=data.channel_names,
            timestamp_offset=data.timestamps[0],
        )


class ChannelSelector(Transform):
    def __call__(
        self,
        data: TimestampedArray,
        channels: list[int] | list[str],
    ) -> TimestampedArray:
        """
        Select specific channels from the data.

        Args:
            data (TimestampedArray): Input TimestampedArray array object
            channels (list[int] | list[str]):
                List of channel indices or channel names to select

        Returns:
            TimestampedArray: TimestampedArray object with only the selected channels
        """
        return data[:, channels]
