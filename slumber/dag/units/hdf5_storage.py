import time
from collections.abc import AsyncGenerator
from pathlib import Path

import ezmsg.core as ez
import h5py
import numpy as np
from loguru import logger

from slumber import settings
from slumber.dag.utils import PydanticSettings
from slumber.utils.data import ArrayBase
from slumber.utils.hdf5 import (
    DatasetDoesNotExistError,
    HDF5Manager,
)


class Settings(PydanticSettings):
    file_path: Path
    group_name: str
    compression: str = settings["hdf5"]["compression"]


class State(ez.State):
    hdf5_manager: HDF5Manager
    group: h5py.Group


class HDF5Storage(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT = ez.InputStream(ArrayBase)

    def initialize(self) -> None:
        self.STATE.hdf5_manager = HDF5Manager(self.SETTINGS.file_path)
        self.STATE.group = self.STATE.hdf5_manager.create_group(
            self.SETTINGS.group_name
        )

    def shutdown(self):
        self.STATE.hdf5_manager.close()

    @ez.subscriber(INPUT)
    async def store(self, message: ArrayBase) -> AsyncGenerator:
        self.STATE.group.attrs.update(message.attributes)
        for dataset_name, data in message.datasets.items():
            self._store_data(data, dataset_name)

    def _store_data(self, data: np.ndarray, dataset_name: str) -> None:
        if data.size == 0:
            logger.warning(f"Data is empty. Skipping storage of {dataset_name}.")
            return

        start_time = time.time()
        try:
            self.STATE.hdf5_manager.append(
                group_name=self.SETTINGS.group_name,
                dataset_name=dataset_name,
                data=data,
            )
        except DatasetDoesNotExistError:
            logger.info(f"Dataset `{dataset_name}` does not exist. Creating it.")
            self.STATE.hdf5_manager.create_dataset(
                group_name=self.SETTINGS.group_name,
                dataset_name=dataset_name,
                data=data,
                compression=self.SETTINGS.compression,
            )
        logger.info(
            f"Stored data {data.shape} in datast {dataset_name}"
            f" in {time.time() - start_time} seconds."
        )

        # TODO: Handle exceptions to store data in case of errors
