from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import Field

from slumber import settings
from slumber.dag.utils import PydanticSettings
from slumber.data_management.hdf5 import HDF5Manager
from slumber.utils.data import Data


class GroupConfig(PydanticSettings):
    name: str
    attributes: dict[str, Any] = Field(default_factory=dict)


class DatasetConfig(GroupConfig):
    name: str
    dtype: str | list[tuple[str, str]] | None = None
    max_shape: tuple[int | None, ...] | None = None
    compression: str = settings["hdf5"]["compression"]


class Settings(PydanticSettings):
    file_path: Path
    group: GroupConfig
    dataset: DatasetConfig
    buffer_size: int


class HDF5Storage(ez.Unit):
    SETTINGS = Settings
    DATA = ez.InputStream(Data)

    def initialize(self) -> None:
        self._hdf5_manager = HDF5Manager(self.SETTINGS.file_path)
        self._hdf5_manager.create_group(
            group_name=self.SETTINGS.group.name, **self.SETTINGS.group.attributes
        )
        self._buffer: list[Data] = []

    def shutdown(self):
        # TODO: handle data in buffer
        self._hdf5_manager.close()

    @ez.subscriber(DATA)
    async def store(self, data: Data) -> AsyncGenerator:
        self._buffer.append(data)
        if len(self._buffer) >= self.SETTINGS.buffer_size:
            self._store()
            self._buffer = []

    def _store(self):
        data = np.concatenate([data.array for data in self._buffer])

        try:
            self._hdf5_manager.append(
                group_name=self.SETTINGS.group.name,
                dataset_name=self.SETTINGS.dataset.name,
                data=data,
            )
        except ValueError:
            logger.info(
                f"Dataset {self.SETTINGS.dataset.name} does not exist. Creating it."
            )
            sample_rate = self._buffer[0].sample_rate
            self._hdf5_manager.create_dataset(
                group_name=self.SETTINGS.group.name,
                dataset_name=self.SETTINGS.dataset.name,
                data=data,
                dtype=self.SETTINGS.dataset.dtype,
                max_shape=self.SETTINGS.dataset.max_shape,
                compression=self.SETTINGS.dataset.compression,
                sample_rate=sample_rate,
            )
