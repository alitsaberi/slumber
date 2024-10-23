import numpy as np

from slumber.processing.signal_quality import (
    compute_snr,
    detect_flatline,
)  # There is room to include more functions/checks


def evaluate_signal_quality(
        raw_data: np.ndarray, 
        sampling_rate: float = 256,
        duration: float = 10
        ) -> bool:
    """
    Evaluate signal quality by checking SNR and flatline detection
    for both EEG left and right channels.

    Args:
        raw_data (numpy.ndarray): 2D array containing acquired data.

        sampling_rate (float, optional): Sampling rate of the data 
                                        (default: 256 Hz).

        duration (float, optional): Duration in seconds to evaluate 
                                        (default: 10 seconds).

    Returns:
        bool: True if signal quality is acceptable, False if signal quality is poor.
    """

    # Extract the last 'duration' seconds of data
    raw_data_window = raw_data[-duration * sampling_rate :, :]

    # Compute SNR for both channels
    snr_l = compute_snr(raw_data_window[:, 0])  # Left channel
    snr_r = compute_snr(raw_data_window[:, 1])  # Right channel

    # Detect flatlines for both channels
    flatline_l = detect_flatline(
        raw_data_window[:, 0], window_duration=duration
    )  # Left channel
    flatline_r = detect_flatline(
        raw_data_window[:, 1], window_duration=duration
    )  # Right channel

    # Combine results from processing
    return not (snr_l < 0 or snr_r < 0 or flatline_l or flatline_r)
