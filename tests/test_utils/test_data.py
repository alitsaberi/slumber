import copy
from datetime import timedelta

import numpy as np
import pytest

from slumber.utils.data import (
    Data,
    get_all_periods,
    get_all_periods_by_period_length,
    get_periods_by_index,
)


def test_empty_data_initialization():
    with pytest.raises(ValueError):
        Data(array=np.array([]), sample_rate=128)


def test_data_initialization(sample_data):
    assert isinstance(sample_data, Data)
    assert sample_data.array.shape == (3840, 2)
    assert sample_data.sample_rate == 128
    assert sample_data.length == 3840
    assert sample_data.n_channels == 2
    assert sample_data.duration == timedelta(seconds=30)
    assert len(sample_data.channel_names) == 2
    assert sample_data.channel_names == ["channel_0", "channel_1"]
    assert sample_data.index.shape == (3840,)


def test_data_loc(sample_data):
    result = sample_data.loc(channels="channel_0")
    assert result.n_channels == 1
    assert result.channel_names == ["channel_0"]

    result = sample_data.loc(samples=slice(0, 100))
    assert result.length == 100
    assert result.n_channels == 2


def test_data_iloc(sample_data):
    result = sample_data.iloc(channels=0)
    assert result.n_channels == 1
    assert result.channel_names == ["channel_0"]

    result = sample_data.iloc(samples=slice(0, 100))
    assert result.length == 100
    assert result.n_channels == 2


def test_data_slice_all_channels(sample_data):
    sliced_data = sample_data[0:100]
    assert sliced_data.length == 100
    assert sliced_data.n_channels == sample_data.n_channels
    assert sliced_data.channel_names == sample_data.channel_names


def test_data_slice_by_channel_names(sample_data):
    channels = ["channel_0"]
    sliced_data = sample_data[0:100, channels]
    assert sliced_data.length == 100
    assert sliced_data.n_channels == len(channels)
    assert sliced_data.channel_names == channels


def test_data_slice_by_channel_indices(sample_data):
    channels = [0, 1]
    expected_channel_names = [sample_data.channel_names[i] for i in channels]
    sliced_data = sample_data[0:100, channels]
    assert sliced_data.length == 100
    assert sliced_data.n_channels == len(channels)
    assert sliced_data.channel_names == expected_channel_names


def test_data_slice_single_channel_by_name(sample_data):
    channel = "channel_0"
    sliced_data = sample_data[0:100, channel]
    assert sliced_data.length == 100
    assert sliced_data.n_channels == 1
    assert sliced_data.channel_names == [channel]


def test_data_slice_single_channel_by_index(sample_data):
    channel_idx = 0
    expected_channel_name = sample_data.channel_names[channel_idx]
    sliced_data = sample_data[0:100, channel_idx]
    assert sliced_data.length == 100
    assert sliced_data.n_channels == 1
    assert sliced_data.channel_names == [expected_channel_name]


@pytest.mark.parametrize(
    "array_shape, channel_names",
    [
        ((100, 2), ["EEG1"]),  # Too few names
        ((100, 2), ["EEG1", "EEG2", "EEG3"]),  # Too many names
    ],
)
def test_data_invalid_channel_names(array_shape, channel_names):
    with pytest.raises(ValueError):
        Data(
            array=np.random.rand(*array_shape),
            sample_rate=128,
            channel_names=channel_names,
        )


def test_get_all_periods_by_period_length(sample_data):
    periods = get_all_periods_by_period_length(sample_data, 10)
    assert periods.shape == (3, 1280, 2)


def test_get_all_periods(sample_data):
    periods = get_all_periods(sample_data, 1280)
    assert periods.shape == (3, 1280, 2)


@pytest.mark.parametrize(
    "start_index, n_samples_per_period, n_periods, expected_shape",
    [
        (0, 1280, 2, (2, 1280, 2)),
        (0, 1280, 2, (2, 1280, 2)),
        (0, 1280, None, (3, 1280, 2)),
        (1, 1280, None, (2, 1280, 2)),
    ],
)
def test_get_periods_by_index(
    sample_data,
    start_index,
    n_samples_per_period,
    n_periods,
    expected_shape,
):
    periods = get_periods_by_index(
        sample_data,
        start_index,
        n_samples_per_period,
        n_periods,
    )
    assert periods.shape == expected_shape


@pytest.mark.parametrize(
    "start_index, n_samples_per_period, n_periods, exception",
    [
        (0, 200, None, ValueError),
        (3, 1280, None, ValueError),
        (0, 1280, 4, ValueError),
    ],
)
def test_get_periods_by_index_raises_error(
    sample_data,
    start_index,
    n_samples_per_period,
    n_periods,
    exception,
):
    with pytest.raises(exception):
        get_periods_by_index(
            sample_data,
            start_index,
            n_samples_per_period,
            n_periods,
        )


def test_data_slice_assignment(sample_data):
    data = copy.deepcopy(sample_data)

    data[0:100] = 1.0
    assert np.all(data.array[0:100] == 1.0)

    data[0:100, "channel_0"] = 2.0
    assert np.all(data.array[0:100, 0] == 2.0)

    data[100:200, ["channel_0", "channel_1"]] = 3.0
    assert np.all(data.array[100:200] == 3.0)

    data[200:300, 0] = 4.0
    assert np.all(data.array[200:300, 0] == 4.0)
