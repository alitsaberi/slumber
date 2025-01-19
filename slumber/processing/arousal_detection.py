import numpy as np
from scipy.ndimage import uniform_filter1d

from slumber import settings
from slumber.utils.data import Data, Event

DEFAULTS = settings["arousal_detection"]
SLEEP_SCORING_LABELS = settings["sleep_scoring"]["labels"]


def detect_arousals(
    scores: Data,
    wake_n1_threshold: float = DEFAULTS["wake_n1_threshold"],
    min_duration: float = DEFAULTS["min_duration"],
    max_duration: float = DEFAULTS["max_duration"],
    merge_gap: float = DEFAULTS["merge_gap"],
    smoothing_window: float = DEFAULTS["smoothing_window"],
    min_transition_increase: float = DEFAULTS["min_transition_increase"],
    gap_threshold_factor: float = DEFAULTS["gap_threshold_factor"],
) -> list[Event]:
    """
    Detect arousals in sleep confidence

    Parameters:
        scores (Data): Sleep scores (high frequency confidence values).
                       The first column is Wake and the second column is N1.
        wake_n1_threshold (float): Threshold for Wake + N1 confidence.
        min_duration (float): Minimum arousal duration in seconds.
        max_duration (float): Maximum arousal duration in seconds.
        merge_gap (float): Maximum gap between consecutive arousals to merge (seconds).
        smoothing_window (int): Window size for smoothing confidence scores (seconds).
        min_transition_increase (float): Minimum increase for transitions to Wake/N1.

    Returns:
        list of arousal events.
    """

    if scores.sample_rate < 1:
        raise ValueError("Sample rate of scores must be at least 1.")

    if scores.duration.total_seconds() < min_duration:
        raise ValueError(
            f"Scores duration {scores.duration.total_seconds()} (sec)"
            " is less than the minimum duration"
            f" {min_duration} (sec)"
        )

    if (
        SLEEP_SCORING_LABELS["wake"] not in scores.channel_names
        or SLEEP_SCORING_LABELS["n1"] not in scores.channel_names
    ):
        raise ValueError("Scores must contain Wake and N1 channels")

    wake_n1_confidence = _prepare_confidence_scores(scores, smoothing_window)

    min_samples = int(min_duration * scores.sample_rate)
    max_samples = int(max_duration * scores.sample_rate)
    merge_gap_samples = int(merge_gap * scores.sample_rate)

    intervals = _find_candidate_intervals(
        wake_n1_confidence,
        wake_n1_threshold,
        min_transition_increase,
    )

    intervals = _merge_nearby_intervals(
        intervals,
        wake_n1_confidence,
        wake_n1_threshold,
        gap_threshold_factor,
        merge_gap_samples,
    )

    return [
        Event(
            label=DEFAULTS["arousal_label"],
            start_time=scores.timestamps[start_index],
            end_time=scores.timestamps[end_index],
        )
        for start_index, end_index in intervals
        if end_index - start_index >= min_samples
        and end_index - start_index <= max_samples
    ]


def _prepare_confidence_scores(data: Data, smoothing_window: float) -> np.ndarray:
    """Prepare and smooth confidence scores."""
    confidence_scores = data[
        :,
        [
            SLEEP_SCORING_LABELS["wake"],
            SLEEP_SCORING_LABELS["n1"],
        ],
    ]
    wake_n1_confidence = np.sum(confidence_scores.array, axis=1)
    return uniform_filter1d(
        wake_n1_confidence, size=int(smoothing_window * data.sample_rate)
    )


def _find_candidate_intervals(
    wake_n1_confidence: np.ndarray,
    wake_n1_threshold: float,
    min_transition_increase: float,
) -> list[tuple[int, int]]:
    """Find initial candidate arousal intervals."""
    arousal_candidates = wake_n1_confidence > wake_n1_threshold
    transitions = np.concatenate(
        ([False], np.diff(wake_n1_confidence) > min_transition_increase)
    )

    condition = arousal_candidates | transitions
    change_points = np.where(np.diff(condition.astype(int)))[0]

    # If odd number of change points, add the end of array as final point
    if len(change_points) % 2:
        change_points = np.append(change_points, len(wake_n1_confidence))

    # Convert change points to intervals
    return list(zip(change_points[::2], change_points[1::2], strict=True))


def _merge_nearby_intervals(
    intervals: list[tuple[int, int]],
    wake_n1_confidence: np.ndarray,
    wake_n1_threshold: float,
    gap_threshold_factor: float,
    merge_gap_samples: int,
) -> list[tuple[int, int]]:
    """Merge intervals that are close together based on confidence in gaps."""
    if not intervals:
        return []

    merged = [intervals[0]]

    for current in intervals[1:]:
        gap_start = merged[-1][1]
        gap_end = current[0]
        gap_confidence = wake_n1_confidence[gap_start:gap_end]

        if (gap_end > gap_start + merge_gap_samples) or max(
            gap_confidence
        ) < wake_n1_threshold * gap_threshold_factor:
            merged.append(current)
            continue

        merged[-1] = (merged[-1][0], current[1])

    return merged
