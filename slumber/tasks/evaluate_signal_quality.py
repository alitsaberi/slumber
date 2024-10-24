import numpy as np

from slumber.processing.signal_quality import (
    compute_snr,
    detect_flatline,
)  # There is room to include more functions/checks


def evaluate_signal_quality(
    raw_data: np.ndarray, sampling_rate: float = 256, duration: float = 10
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

    # TODO: Change 0 and 1 to channel names (e.g., EEG_L and EEG_R)
    # TODO: Check to only include measurements that are recorded (e.g., EEG,
    #       heart rate, etc.)
    # TODO: Determine whether to add the thresholds for SNR and flatline detection 
    #       in this function

    # Compute SNR for both channels
    snr_l_below_threshold = compute_snr(
        eeg_data=raw_data_window[:, 0], sampling_rate=sampling_rate, snr_threshold_db=0
    )  # Left channel
    snr_r_below_threshold = compute_snr(
        eeg_data=raw_data_window[:, 1], sampling_rate=sampling_rate, snr_threshold_db=0
    )  # Right channel

    # Detect flatlines for both channels
    flatline_l = detect_flatline(
        eeg_data=raw_data_window[:, 0], sampling_rate=sampling_rate
    )  # Left channel
    flatline_r = detect_flatline(
        eeg_data=raw_data_window[:, 1], sampling_rate=sampling_rate
    )  # Right channel

    # Combine results from processing
    return not (
        snr_l_below_threshold or snr_r_below_threshold or flatline_l or flatline_r
    )
