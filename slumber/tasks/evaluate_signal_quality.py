import numpy as np

from slumber.processing.signal_quality import (
    compute_snr,
    detect_flatline,
)  # There is room to include more functions/checks


def evaluate_signal_quality(raw_data: np.ndarray, sample_rate: float) -> bool:
    """
    Evaluate signal quality by checking SNR and flatline detection
    for both EEG left and right channels.

    Args:
        raw_data (numpy.ndarray): 2D array containing acquired data.

        sample_rate (float): Sampling rate of the data.

    Returns:
        bool: True if signal quality is acceptable, False if signal quality is poor.
    """

    # TODO: Change 0 and 1 to channel names (e.g., EEG_L and EEG_R)
    # TODO: Check to only include measurements that are recorded (e.g., EEG,
    #       heart rate, etc.)
    # TODO: Determine whether to add the thresholds for SNR and flatline detection
    #       in this function

    # Compute SNR for both channels
    snr_l_below_threshold = compute_snr(
        eeg_data=raw_data[:, 0], sampling_rate=sample_rate, snr_threshold_db=0
    )  # Left channel
    snr_r_below_threshold = compute_snr(
        eeg_data=raw_data[:, 1], sampling_rate=sample_rate, snr_threshold_db=0
    )  # Right channel

    # Detect flatlines for both channels
    flatline_l = detect_flatline(
        eeg_data=raw_data[:, 0], sampling_rate=sample_rate
    )  # Left channel
    flatline_r = detect_flatline(
        eeg_data=raw_data[:, 1], sampling_rate=sample_rate
    )  # Right channel

    # Combine results from processing
    return not (
        snr_l_below_threshold or snr_r_below_threshold or flatline_l or flatline_r
    )
