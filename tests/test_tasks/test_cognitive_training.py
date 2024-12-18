from pathlib import Path
from unittest.mock import Mock

import pytest
from pyttsx3 import Engine

from slumber.sources.zmax import ZMax
from slumber.tasks.cognitive_training import (
    CognitiveTrainingConfig,
    create_action,
    execute_cognitive_training,
)
from slumber.utils.helpers import load_yaml


@pytest.fixture
def mock_text2speech_engine():
    engine = Mock(spec=Engine)
    engine.getProperty.return_value = 0.5
    return engine


@pytest.fixture
def mock_zmax():
    return Mock(spec=ZMax)


@pytest.fixture
def mock_cognitive_training_config(mock_text2speech_engine, mock_zmax):
    return CognitiveTrainingConfig(
        zmax=mock_zmax,
        text2speech_engine=mock_text2speech_engine,
        min_subjective_light_intensity=50,
        min_subjective_volume=0.5,
    )


def test_sample_cognitive_training_protocol(mock_cognitive_training_config):
    protocol_file = (
        Path(__file__).parents[1] / "resources" / "sample_cognitive_training.yaml"
    )
    protocol = load_yaml(protocol_file)
    protocol = [create_action(**action_config) for action_config in protocol]
    execute_cognitive_training(protocol, mock_cognitive_training_config)


def test_create_action_invalid_type():
    with pytest.raises(ValueError):
        create_action("InvalidAction")


def test_execute_cognitive_training_empty_protocol(mock_cognitive_training_config):
    with pytest.raises(ValueError, match="Protocol cannot be empty"):
        execute_cognitive_training([], mock_cognitive_training_config)
