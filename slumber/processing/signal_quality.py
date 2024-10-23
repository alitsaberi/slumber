import logging

import numpy as np
from scipy.signal import butter, filtfilt

logger = logging.getLogger("slumber")


def compute_snr(
    eeg_data: np.ndarray, 
    sampling_rate: float = 256,
    signal_band: tuple[float, ...] = (0.5, 30),
    noise_band: tuple[float, ...] = (30, 100)
) -> float:
    """
    Calculate the signal-to-noise ratio (SNR) of the EEG signal.

    Args:
        eeg_data (np.ndarray): The EEG channel to analyze.

        sampling_rate (float): The sampling rate of the EEG data in Hz (default: 256 Hz).

        signal_band (tuple): The frequency range for the signal band (default: (0.5, 30) Hz).

        noise_band (tuple): The frequency range for the noise band (default: (30, 100) Hz).

    Returns:
        float: The calculated SNR in dB.
    """

    signal_filtered = filtfilt(*butter(4, signal_band, btype='band', fs=sampling_rate), eeg_data)
    noise_filtered = filtfilt(*butter(4, noise_band, btype='band', fs=sampling_rate), eeg_data)

    # Compute power
    signal_power = np.mean(signal_filtered**2)
    noise_power = np.mean(noise_filtered**2)

    # Compute SNR in dB    
    snr = 10 * np.log10(signal_power / noise_power) if noise_power != 0 else np.inf

    logger.info(f"SNR is {snr}")
    return snr


def detect_flatline(
    eeg_data: np.ndarray, 
    sampling_rate: float = 256,
    flatline_threshold: float =1e-6,
    flatline_duration: int =5,
) -> bool:
    """
    Detects a flatline in the EEG signal.

    Args:
        eeg_data (numpy.ndarray): The EEG channel to analyze.

        sampling_rate (float): The sampling rate of the EEG data in Hz (default: 256 Hz).

        flatline_threshold (float): Maximum allowed change between consecutive samples
                                    to be considered flat (default: 1e-6).

        window_duration (int): Duration of the analysis window in seconds.

        flatline_duration (int): Minimum duration of a flatline in seconds (default: 5).

    Returns:
        bool: True if a flatline is detected in any channel, False otherwise.

    Notes:
        A flatline is detected when the signal change remains below the threshold
        for at least the specified flatline duration within the given window duration.
    """

    flatline_samples = int(
        flatline_duration * sampling_rate
    )  # Number of samples for flatline duration

    diff = np.abs(np.diff(eeg_data, axis=1))

    flatline_detected = np.sum(diff < flatline_threshold, axis=1) >= flatline_samples

    if flatline_detected:
        logger.info("Flatline detected in channel")
    else:
        logger.info("No flatline detected")
    return np.any(flatline_detected)
