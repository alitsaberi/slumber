from typing import Protocol, runtime_checkable

from mne.filter import filter_data

from slumber.utils.data import Data


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


def get_transform_class(class_name: str) -> type[Transform]:
    try:
        transform_class = globals().get(class_name)
        if not issubclass(transform_class, Transform):
            raise ValueError(f"{class_name} is not a subclass of Transform.")
        return transform_class
    except AttributeError as e:
        raise ValueError(
            f"Transform class {class_name} not found in transforms."
        ) from e


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
        data.array = filter_data(
            data.array.T, data.sample_rate, low_cutoff, high_cutoff
        ).T
        return data
