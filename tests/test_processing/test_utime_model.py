from contextlib import nullcontext as does_not_raise
from pathlib import Path

import numpy as np
import pytest
from tensorflow.keras.models import Model
from utime.hyperparameters import YAMLHParams

from slumber.processing.sleep_scoring import UTimeModel, score


@pytest.fixture
def sample_model_dir():
    return Path(__file__).parent.parent / "resources" / "sample_utime_model"


@pytest.fixture
def utime_params():
    return {
        "weight_file_name": "model_weights.h5",
        "n_periods": 3,
        "n_samples_per_prediction": 1280,
    }


@pytest.fixture
def utime_model(sample_model_dir, utime_params):
    return UTimeModel(model_dir=sample_model_dir, **utime_params)


def test_utime_model_initialization(utime_model, sample_model_dir, utime_params):
    assert utime_model._model_dir == sample_model_dir
    assert utime_model._weight_file_name == utime_params["weight_file_name"]
    assert utime_model._n_periods == utime_params["n_periods"]
    assert (
        utime_model.n_samples_per_prediction == utime_params["n_samples_per_prediction"]
    )
    assert utime_model.name == sample_model_dir.name
    assert utime_model._dataset == "dataset"


def test_utime_hyperparameters(utime_model, utime_params):
    assert isinstance(utime_model.hyperparameters, YAMLHParams)
    assert "batch_shape" in utime_model.hyperparameters["build"]
    assert (
        utime_model.hyperparameters["build"]["batch_shape"][1]
        == utime_params["n_periods"]
    )
    assert (
        utime_model.hyperparameters["build"]["data_per_prediction"]
        == utime_params["n_samples_per_prediction"]
    )
    assert utime_model.hyperparameters["build"]["n_classes"] == 5
    assert utime_model.hyperparameters.get("quality_control_func") is not None
    assert utime_model.hyperparameters.get("scaler") is not None
    assert utime_model.hyperparameters.get("set_sample_rate") == 128


def test_utime_model(utime_model):
    assert isinstance(utime_model.model, Model)
    assert (
        list(utime_model.input_shape)
        == utime_model.hyperparameters["build"]["batch_shape"][1:]
    )


def test_prepare_data(utime_model, sample_data):
    prepared_data = utime_model.prepare_data(sample_data)
    assert isinstance(prepared_data, np.ndarray)
    assert prepared_data.dtype == np.float32
    assert prepared_data.shape == (1, 3, 1280, 2)  # 3 periods of 10 seconds at 100 Hz


def test_prepare_data_with_resampling(utime_model, sample_data):
    sample_data.sample_rate = 64  # Different from model's sample rate
    with pytest.raises(ValueError):
        _ = utime_model.prepare_data(sample_data)


@pytest.mark.parametrize(
    "channel_groups, expection",
    [
        ([[0], [1]], does_not_raise()),
        ([[], [2]], pytest.raises(ValueError)),
        ([], pytest.raises(ValueError)),
    ],
)
def test_assert_channel_groups(utime_model, channel_groups, expection):
    with expection:
        utime_model._assert_channel_groups(channel_groups)


def test_predict(utime_model, sample_data):
    prepared_data = utime_model.prepare_data(sample_data)
    channel_groups = [[0], [1]]

    predictions = utime_model.predict(prepared_data, channel_groups)

    assert isinstance(predictions, np.ndarray)
    assert predictions.shape == (
        int(sample_data.length / utime_model.n_samples_per_prediction),
        5,
    )  # 5 classes


def test_predict_with_single_channel_group(utime_model, sample_data):
    prepared_data = utime_model.prepare_data(sample_data)
    channel_groups = [[0]]
    predictions = utime_model.predict(prepared_data, channel_groups)

    assert isinstance(predictions, np.ndarray)
    assert predictions.shape == (
        int(sample_data.length / utime_model.n_samples_per_prediction),
        5,
    )  # 5 classes


def test_predict_with_invalid_group(utime_model, sample_data):
    prepared_data = utime_model.prepare_data(sample_data)
    channel_groups = [[0, 1]]

    with pytest.raises(ValueError):
        _ = utime_model.predict(prepared_data, channel_groups)


def test_score_with_default_channel_groups(sample_data, utime_model):
    with pytest.raises(ValueError):
        score(sample_data, utime_model)


def test_score_with_custom_channel_groups(sample_data, utime_model):
    channel_groups = [[0], [1]]
    result = score(sample_data, utime_model, channel_groups=channel_groups)
    print(result)
    assert isinstance(result, np.ndarray)
    assert result.shape == (3,)
    assert np.all((result >= 0) & (result <= 4))


def test_score_without_argmax(sample_data, utime_model):
    channel_groups = [[0], [1]]
    result = score(
        sample_data, utime_model, channel_groups=channel_groups, arg_max=False
    )
    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 5)  # 3 periods, 5 sleep stages
