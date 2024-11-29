import numpy as np
import pytest

from slumber import settings
from slumber.processing.arousal_detection import detect_arousals
from slumber.utils.data import Data


@pytest.fixture
def sample_scores():
    # Create sample data with known arousals
    duration = 30  # seconds
    sample_rate = 4  # Hz
    n_samples = duration * sample_rate

    # Initialize arrays with low Wake/N1 confidence
    wake = np.zeros(n_samples)
    n1 = np.zeros(n_samples)

    scores = np.column_stack((wake, n1))
    return Data(
        array=scores,
        sample_rate=sample_rate,
        channel_names=[
            settings["sleep_scoring"]["labels"]["wake"],
            settings["sleep_scoring"]["labels"]["n1"],
        ],
    )


def test_detect_arousals_basic(sample_scores):
    scores = sample_scores[:]
    scores[20:32, 0] = 0.6  # 5-8 seconds
    scores[20:32, 1] = 0.2

    scores[60:72, 0] = 0.5  # 15-18 seconds
    scores[60:72, 1] = 0.3

    arousals = detect_arousals(
        scores=scores,
        wake_n1_threshold=0.5,
        min_duration=3.0,
        max_duration=15.0,
        merge_gap=5.0,
        smoothing_window=0.25,
    )

    assert len(arousals) == 2
    # Check first arousal (around 5-8 seconds)
    assert 19 <= arousals[0][0] <= 21  # start index
    assert 31 <= arousals[0][1] <= 33  # end index

    # Check second arousal (around 15-18 seconds)
    assert 59 <= arousals[1][0] <= 61
    assert 71 <= arousals[1][1] <= 73


def test_detect_arousals_merge(sample_scores):
    scores = sample_scores[:]

    # Two arousals with small gap
    scores[20:28, 0] = 0.6
    scores[32:40, 0] = 0.6
    scores[20:28, 1] = 0.2
    scores[32:40, 1] = 0.2

    arousals = detect_arousals(
        scores=scores,
        wake_n1_threshold=0.5,
        merge_gap=2.0,  # should merge events within 2 seconds
        smoothing_window=0.25,
        gap_threshold_factor=0,
    )

    assert len(arousals) == 1  # Two arousals should be merged
    assert 19 <= arousals[0][0] <= 21
    assert 39 <= arousals[0][1] <= 41


def test_detect_arousals_duration_limits(sample_scores):
    scores = sample_scores[:]

    # Too short arousal (1 second)
    scores[20:24, 0] = 0.6
    scores[20:24, 1] = 0.2

    # Too long arousal (16 seconds)
    scores[40:104, 0] = 0.6
    scores[40:104, 1] = 0.2

    arousals = detect_arousals(
        scores=scores,
        min_duration=3.0,
        max_duration=15.0,
        smoothing_window=0.25,
    )

    assert len(arousals) == 0  # Both arousals should be filtered out


def test_invalid_scores():
    scores = Data(
        array=np.zeros((100, 2)),
        sample_rate=0.5,
        channel_names=[
            settings["sleep_scoring"]["labels"]["wake"],
            settings["sleep_scoring"]["labels"]["n1"],
        ],
    )

    with pytest.raises(ValueError, match="Sample rate of scores must be at least 1"):
        detect_arousals(scores)

    scores = Data(array=np.zeros((100, 2)), sample_rate=0.5)

    with pytest.raises(ValueError, match=""):
        detect_arousals(scores)


def test_empty_data(sample_scores):
    arousals = detect_arousals(sample_scores)
    assert len(arousals) == 0
