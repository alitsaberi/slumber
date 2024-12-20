import numpy as np
import pytest

from slumber.utils.hdf5 import HDF5Manager


@pytest.fixture
def temp_hdf5_file(tmp_path):
    return tmp_path / "test.h5"


@pytest.fixture
def hdf5_manager(temp_hdf5_file):
    return HDF5Manager(temp_hdf5_file)


def test_hdf5_manager_initialization(temp_hdf5_file, hdf5_manager):
    assert hdf5_manager._file_path == temp_hdf5_file


def test_context_manager(hdf5_manager):
    try:
        with hdf5_manager as manager:
            raise RuntimeError("Test error")
    except RuntimeError:
        assert manager._file.id.valid == 0  # 0 means file is closed


def test_create_group(hdf5_manager):
    with hdf5_manager as manager:
        group = manager.create_group("test_group", attr1="value1")
        assert "test_group" in manager.groups
        assert group.attrs["attr1"] == "value1"


def test_create_dataset_with_data(hdf5_manager):
    with hdf5_manager as manager:
        manager.create_group("test_group")
        data = np.random.rand(100, 2)
        dataset = manager.create_dataset(
            "test_group", "test_dataset", data=data, sampling_rate=128
        )
        assert dataset.shape == (100, 2)
        assert dataset.attrs["sampling_rate"] == 128


def test_create_dataset_with_shape(hdf5_manager):
    with hdf5_manager as manager:
        manager.create_group("test_group")
        shape = (1000, 2)
        dataset = manager.create_dataset(
            "test_group", "test_dataset", shape=shape, dtype="float64"
        )
        assert dataset.shape == shape


def test_append_data(hdf5_manager):
    with hdf5_manager as manager:
        manager.create_group("test_group")
        initial_data = np.random.rand(100, 2)
        dataset = manager.create_dataset(
            "test_group", "test_dataset", data=initial_data, max_shape=(None, 2)
        )

        append_data = np.random.rand(50, 2)
        manager.append("test_group", "test_dataset", append_data)
        assert dataset.shape == (150, 2)


@pytest.mark.parametrize(
    "group_name, dataset_name, data, shape, error",
    [
        ("nonexistent", "test", np.random.rand(10, 2), None, ValueError),
        ("test_group", "test", None, None, ValueError),
        ("test_group", "test", np.random.rand(10, 2, 2), None, ValueError),
    ],
)
def test_create_dataset_errors(
    hdf5_manager, group_name, dataset_name, data, shape, error
):
    with hdf5_manager as manager:
        if group_name == "test_group":
            manager.create_group(group_name)
        with pytest.raises(error):
            manager.create_dataset(group_name, dataset_name, data=data, shape=shape)


def test_get_dataset(hdf5_manager):
    with hdf5_manager as manager:
        manager.create_group("test_group")
        data = np.random.rand(100, 2)
        manager.create_dataset("test_group", "test_dataset", data=data)
        dataset = manager.get_dataset("test_group", "test_dataset")
        assert np.array_equal(dataset[:], data)
