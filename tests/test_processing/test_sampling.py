import numpy as np
import pytest

from slumber.processing.sampling import fourier_resample, poly_resample, resample


@pytest.fixture
def sample_data():
    return np.random.rand(1000, 2)


def test_fourier_resample(sample_data):
    old_sample_rate = 1000
    new_sample_rate = 500
    resampled_data = fourier_resample(sample_data, new_sample_rate, old_sample_rate)
    assert resampled_data.shape[0] == 500
    assert resampled_data.shape[1] == sample_data.shape[1]


def test_poly_resample(sample_data):
    old_sample_rate = 1000
    new_sample_rate = 500
    resampled_data = poly_resample(sample_data, new_sample_rate, old_sample_rate)
    assert resampled_data.shape[0] == 500
    assert resampled_data.shape[1] == sample_data.shape[1]


def test_resample_poly_method(sample_data):
    old_sample_rate = 1000
    new_sample_rate = 500
    resampled_data = resample(
        sample_data, new_sample_rate, old_sample_rate, method="poly"
    )
    assert resampled_data.shape[0] == 500
    assert resampled_data.shape[1] == sample_data.shape[1]


def test_resample_fourier_method(sample_data):
    old_sample_rate = 1000
    new_sample_rate = 500
    resampled_data = resample(
        sample_data, new_sample_rate, old_sample_rate, method="fourier"
    )
    assert resampled_data.shape[0] == 500
    assert resampled_data.shape[1] == sample_data.shape[1]


def test_resample_invalid_method(sample_data):
    old_sample_rate = 1000
    new_sample_rate = 500
    with pytest.raises(AttributeError):
        resample(sample_data, new_sample_rate, old_sample_rate, method="invalid")


def test_resample_upsample(sample_data):
    old_sample_rate = 500
    new_sample_rate = 1000
    resampled_data = resample(sample_data, new_sample_rate, old_sample_rate)
    assert resampled_data.shape[0] == 2000
    assert resampled_data.shape[1] == sample_data.shape[1]


def test_resample_same_rate(sample_data):
    sample_rate = 1000
    resampled_data = resample(sample_data, sample_rate, sample_rate)
    np.testing.assert_array_almost_equal(resampled_data, sample_data)
