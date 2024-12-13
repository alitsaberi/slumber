import ezmsg.core as ez
import pytest
from pydantic import ValidationError

from slumber.dag.units.sleep_scoring import (
    Settings,
    SleepScoring,
    TransformConfig,
)
from slumber.processing.transforms import FIRFilter


@pytest.fixture
def sample_transform_dict(sample_collection_config):
    return sample_collection_config["sleep_scoring"]["settings"]["transforms"][0]


@pytest.fixture
def sample_model_dict(sample_collection_config):
    return sample_collection_config["sleep_scoring"]["settings"]["model"]


@pytest.fixture
def sample_settings(sample_collection_config):
    return Settings.model_validate(
        sample_collection_config["sleep_scoring"]["settings"]
    )


def test_transform_config(sample_transform_dict):
    transform_config = TransformConfig.model_validate(sample_transform_dict)
    assert transform_config.channel_indices == [0, 1]
    assert transform_config.target_channel_indices == [0, 1]
    assert isinstance(transform_config.transform, FIRFilter)
    assert transform_config.kwargs == {"low_cutoff": 0.3, "high_cutoff": 30}


@pytest.mark.parametrize(
    "dict_update",
    [
        ({"channel_indices": [0]}),
        ({"target_channel_indices": [0]}),
        ({"class_name": "FakeTransform"}),
        ({"channel_indices": [], "target_channel_indices": []}),
    ],
)
def test_transform_config_validation_errors(sample_transform_dict, dict_update):
    sample_transform_dict.update(dict_update)
    with pytest.raises(ValidationError):
        TransformConfig.model_validate(sample_transform_dict)


@pytest.mark.parametrize(
    "transform_configs,expected_error",
    [
        (
            [
                {
                    "channel_indices": [0, 1],
                    "target_channel_indices": [0, 1],
                    "class_name": "FIRFilter",
                },
                {
                    "channel_indices": [2, 3],
                    "target_channel_indices": [0, 1],
                    "class_name": "FIRFilter",
                },
            ],
            "Target channel indices {0, 1} are used in multiple transforms",
        ),
        (
            [
                {
                    "channel_indices": [0, 1],
                    "target_channel_indices": [0, 2],
                    "class_name": "FIRFilter",
                },
                {
                    "channel_indices": [2, 3],
                    "target_channel_indices": [3, 4],
                    "class_name": "FIRFilter",
                },
            ],
            "Target channel indices must be consecutive integers starting from 0",
        ),
    ],
)
def test_settings_validate_target_channel_indices(
    sample_collection_config, transform_configs, expected_error
):
    config = sample_collection_config["sleep_scoring"]["settings"]
    config["transforms"] = transform_configs

    with pytest.raises(ValueError, match=expected_error):
        Settings.model_validate(config)


def test_settings_valid_target_channel_indices(sample_collection_config):
    config = sample_collection_config["sleep_scoring"]["settings"]
    config["transforms"] = [
        {
            "channel_indices": [0, 1],
            "target_channel_indices": [0, 1],
            "class_name": "FIRFilter",
        },
        {
            "channel_indices": [2, 3],
            "target_channel_indices": [2, 3],
            "class_name": "FIRFilter",
        },
    ]

    settings = Settings.model_validate(config)
    assert settings.all_indices == [0, 1, 2, 3]


@pytest.fixture
def test_collection(dummy_data_generator, sample_settings):
    class TestCollection(ez.Collection):
        DATA_GEN = dummy_data_generator
        SLEEP_SCORING = SleepScoring()

        def configure(self) -> None:
            self.SLEEP_SCORING.apply_settings(sample_settings)

        def network(self) -> ez.NetworkDefinition:
            return ((self.DATA_GEN.OUTPUT_DATA, self.SLEEP_SCORING.INPUT_DATA),)

    return TestCollection()


def test_sleep_scoring_unit(test_collection):
    ez.run(test_collection)
