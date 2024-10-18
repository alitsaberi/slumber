from datetime import timedelta

import numpy as np
import pytest

from slumber.processing.sleep_scoring import Data


@pytest.fixture
def sample_data():
    return Data(
        array=np.random.rand(3 * 10 * 128, 2),
        sample_rate=128,
    )


def test_data_initialization(sample_data):
    assert isinstance(sample_data, Data)
    assert sample_data.array.shape == (3840, 2)
    assert sample_data.sample_rate == 128
    assert sample_data.length == 3840
    assert sample_data.n_channels == 2
    assert sample_data.duration == timedelta(seconds=30)


def test_get_all_periods_by_period_length(sample_data):
    periods = sample_data.get_all_periods_by_period_length(10)
    assert periods.shape == (3, 1280, 2)


def test_get_all_periods(sample_data):
    periods = sample_data.get_all_periods(1280)
    assert periods.shape == (3, 1280, 2)


@pytest.mark.parametrize(
    "start_index, n_samples_per_period, n_periods, channel_indices, expected_shape",
    [
        (0, 1280, 2, None, (2, 1280, 2)),
        (0, 1280, 2, [0], (2, 1280, 1)),
        (0, 1280, None, None, (3, 1280, 2)),
        (1, 1280, None, None, (2, 1280, 2)),
    ],
)
def test_get_periods_by_index(
    sample_data,
    start_index,
    n_samples_per_period,
    n_periods,
    channel_indices,
    expected_shape,
):
    periods = sample_data.get_periods_by_index(
        start_index, n_samples_per_period, n_periods, channel_indices=channel_indices
    )
    assert periods.shape == expected_shape


@pytest.mark.parametrize(
    "start_index, n_samples_per_period, n_periods, channel_indices, exception",
    [
        (0, 200, None, None, ValueError),
        (3, 1280, None, None, ValueError),
        (0, 1280, 4, None, ValueError),
        (0, 1280, None, [1, 2, 3], IndexError),
    ],
)
def test_get_periods_by_index_raises_error(
    sample_data,
    start_index,
    n_samples_per_period,
    n_periods,
    channel_indices,
    exception,
):
    with pytest.raises(exception):
        sample_data.get_periods_by_index(
            start_index,
            n_samples_per_period,
            n_periods,
            channel_indices=channel_indices,
        )
