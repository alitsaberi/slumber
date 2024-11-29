import types
from pathlib import Path

import h5py
import numpy as np
from loguru import logger

from slumber import settings


# TODO: Move this to utils and remove data_management
class HDF5Manager:
    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._file = h5py.File(self._file_path, "a")

    def __enter__(self) -> "HDF5Manager":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._file.id:
            self._file.close()

    @property
    def groups(self) -> list[str]:
        return list(self._file.keys())

    def create_group(self, group_name: str, **attributes) -> h5py.Group:
        group = self._file.create_group(group_name)
        group.attrs.update(attributes)
        return group

    def create_dataset(
        self,
        group_name: str,
        dataset_name: str,
        data: np.ndarray | None = None,
        shape: tuple[int, ...] | None = None,
        dtype: str | list[tuple[str, str]] | None = None,
        max_shape: tuple[int | None, ...] | None = None,
        compression: str = settings["hdf5"]["compression"],
        **attributes,
    ) -> h5py.Dataset:
        """
        Create a dataset in the HDF5 file.

        Args:
            group_name (str): The name of the group to create the dataset in.
            dataset_name (str): The name of the dataset to create.
            data (np.ndarray | None, optional):
                The data to store in the dataset. Defaults to None.
            shape (tuple[int, ...] | None, optional):
                The shape of the dataset. Defaults to None.
            dtype (str | list[tuple[str, str]] | None, optional):
                The data type of the dataset.
                Defaults to None.
                To define field names, use a list of tuples (field_name, field_type).
            max_shape (tuple[int | None, ...] | None, optional):
                The maximum shape of the dataset. Defaults to None.
            compression (str, optional): The compression algorithm to use.
                Defaults to settings["hdf5"]["compression"].
            **attributes (dict, optional):
            Additional attributes to store in the dataset.

        Returns:
            h5py.Dataset: The created dataset.
        """
        if group_name not in self._file:
            raise ValueError(f"Group {group_name} does not exist.")

        if data is None and shape is None:
            raise ValueError("Either data or shape must be provided.")

        if (data is not None and len(data.shape) > 2) or (
            shape is not None and len(shape) > 2
        ):
            raise ValueError(
                "Data must be a 1D or 2D array. Shape must be a 1D or 2D array."
                f" Shape: {data.shape if data is not None else shape}"
            )

        max_shape = max_shape or len(data.shape if data is not None else shape) * (
            None,
        )
        dataset = self._file[group_name].create_dataset(
            dataset_name,
            data=data,
            shape=shape,
            dtype=dtype,
            maxshape=max_shape,
            compression=compression,
        )
        dataset.attrs.update(attributes)
        return dataset

    def get_dataset(self, group_name: str, dataset_name: str) -> h5py.Dataset:
        return self._file[group_name][dataset_name]

    def append(self, group_name: str, dataset_name: str, data: np.ndarray) -> None:
        if group_name not in self._file:
            raise ValueError(f"Group {group_name} does not exist.")

        if dataset_name not in self._file[group_name]:
            raise ValueError(
                f"Dataset {dataset_name} does not exist in group {group_name}."
            )

        dataset = self._file[group_name][dataset_name]
        logger.debug(
            f"Appending data to dataset {dataset_name} in group {group_name}"
            f" with shape {dataset.shape}."
        )

        if dataset.ndim == 2 and dataset.shape[1] != data.shape[1]:
            raise ValueError(
                f"Data must have the same number of channels as the dataset."
                f" Dataset shape: {dataset.shape}, Data shape: {data.shape}"
            )

        dataset.resize(dataset.shape[0] + len(data), axis=0)
        dataset[-len(data) :] = data

        logger.debug(
            f"Data appended to dataset {dataset_name} in group {group_name}."
            f" The new shape is {dataset.shape}."
        )
