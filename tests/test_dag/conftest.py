import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import ezmsg.core as ez
import numpy as np
import pytest
import yaml

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import Data


@pytest.fixture
def sample_collection_config():
    config_path = Path("tests/resources/sample_collection.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


class DummyDataGeneratorSetting(PydanticSettings):
    sample_rate: int = 256
    duration: int = 10
    n_channels: int = 2
    n_iterations: int = 5


@pytest.fixture
def dummy_data_generator():
    class DummyDataGenerator(ez.Unit):
        SETTINGS = DummyDataGeneratorSetting

        OUTPUT_DATA = ez.OutputStream(Data)

        @ez.publisher(OUTPUT_DATA)
        async def generate_data(self) -> AsyncGenerator:
            for _ in range(self.SETTINGS.n_iterations):
                t = np.linspace(
                    0,
                    self.SETTINGS.duration,
                    self.SETTINGS.sample_rate * self.SETTINGS.duration,
                )
                data = np.zeros((len(t), self.SETTINGS.n_channels))
                for i in range(self.SETTINGS.n_channels):
                    data[:, i] = np.sin(2 * np.pi * (i + 1) * t)

                yield self.OUTPUT_DATA, Data(data, self.SETTINGS.sample_rate)
                await asyncio.sleep(0.1)

            raise ez.NormalTermination

    return DummyDataGenerator()
