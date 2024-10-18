import logging

import numpy as np
from mne.filter import resample as mne_resample
from scipy.signal import resample_poly as scipy_resample

logger = logging.getLogger("slumber")


def fourier_resample(
    data: np.ndarray, new_sample_rate: int, old_sample_rate: int
) -> np.ndarray:
    return mne_resample(
        data.astype(np.float64), new_sample_rate, old_sample_rate, axis=0
    )


def poly_resample(
    data: np.ndarray, new_sample_rate: int, old_sample_rate: int
) -> np.ndarray:
    return scipy_resample(data, new_sample_rate, old_sample_rate, axis=0)


def resample(
    data: np.ndarray, new_sample_rate: int, old_sample_rate: int, method: str = "poly"
):
    resample_function = getattr(
        __import__(__name__, fromlist=[f"{method}_resample"]),
        f"{method}_resample",
    )

    return resample_function(data, new_sample_rate, old_sample_rate)
