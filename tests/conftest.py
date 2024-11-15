import numpy as np
import pytest

from slumber.utils.data import Data


@pytest.fixture
def sample_data():
    return Data(
        array=np.random.rand(3 * 10 * 128, 2),
        sample_rate=128,
    )
