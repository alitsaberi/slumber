import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen
from time import sleep

import mne
import numpy as np
import psutil
from loguru import logger

from slumber import settings
from slumber.utils.data import Data

from .constants import (
    DEFAULTS,
    FILE_EXTENSION,
    HYPNODYNE_PROCESSES,
    MAX_VOLTAGE,
    MIN_VOLTAGE,
    QUICKSTART_APP_NAME,
    SAMPLE_RATE,
)


def _read_raw_data(data_dir: Path, data_type: str) -> mne.io.Raw:
    logger.info(f"Extracting {data_type}")
    data_type_file = data_dir / f"{data_type}.{FILE_EXTENSION}"
    raw = mne.io.read_raw_edf(data_type_file, preload=False)
    return raw.get_data().squeeze()


def load_data(data_dir: Path, data_types: list[str]) -> Data:
    array = np.column_stack(
        [_read_raw_data(data_dir, data_type) for data_type in data_types]
    )
    data = Data(array, sample_rate=SAMPLE_RATE, channel_names=data_types)
    logger.debug(f"Loaded data: {data}")
    return data


def get_word_at(buffer: str, index: int) -> int:
    return get_byte_at(buffer, index) * 256 + get_byte_at(buffer, index + 1)


def get_byte_at(buffer: str, index: int) -> int:
    hex_str = buffer[index * 3 : index * 3 + 2]
    return int(hex_str, 16)


def scale_eeg(value: int) -> float:
    """
    Convert the raw EEG value to uV.
    """
    uv_range = 3952
    return ((value - 32768) * uv_range) / 65536


def scale_accelerometer(value: int) -> float:
    """
    Convert the raw accelerometer value to 'g'.
    """
    return value * 4 / 4096 - 2


def scale_battery(value: int) -> float:
    """
    Convert the raw battery voltage value to volts.
    """
    return value / 1024 * 6.60


def scale_body_temperature(value: int) -> float:
    """
    Convert the raw body temperature value to Celsius.
    """
    return 15 + ((value / 1024 * 3.3 - 1.0446) / 0.0565537333333333)


def dec2hex(decimal: int, pad: int = 2) -> str:
    """Convert decimal to hexadecimal string with padding."""
    return format(decimal, f"0{pad}x").upper()


def voltage_to_percentage(voltage: float) -> int:
    voltage = max(MIN_VOLTAGE, min(voltage, MAX_VOLTAGE))
    percentage = ((voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE)) * 100
    return round(percentage)


def verify_hypnodyne_processes(timeout: int = 30) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        running_processes = {
            proc.info["name"]
            for proc in psutil.process_iter(["name"])
            if proc.info["name"] in HYPNODYNE_PROCESSES
        }

        if running_processes == set(HYPNODYNE_PROCESSES):
            logger.info("All Hypnodyne processes running")
            return True

        sleep(1)

    missing = set(HYPNODYNE_PROCESSES) - running_processes
    logger.error(f"Missing Hypnodyne processes: {missing}")
    return False


def close_all_hypnodyne_processes():
    for process_name in HYPNODYNE_PROCESSES:
        while True:
            processes = [
                proc
                for proc in psutil.process_iter(["name"])
                if proc.info["name"] == process_name
            ]
            if not processes:
                break

            for proc in processes:
                try:
                    proc.terminate()
                    proc.wait(settings["process_termination_timeout"])
                    logger.info(f"Terminated {process_name} with PID {proc.pid}")
                except psutil.TimeoutExpired:
                    proc.kill()
                    logger.warning(f"Force killed {process_name} with PID {proc.pid}")
                except psutil.NoSuchProcess:
                    pass


def open_quick_start(max_retries: int = 3, retry_delay: float = 2.0) -> Popen:
    hypnodyne_suite_directory = Path(DEFAULTS["hypnodyne_suite_directory"])
    quick_start_path = hypnodyne_suite_directory / QUICKSTART_APP_NAME

    if not quick_start_path.exists():
        raise FileNotFoundError(
            f"QuickStart executable not found at {quick_start_path}"
        )

    for attempt in range(max_retries):
        try:
            close_all_hypnodyne_processes()

            process = Popen(
                [str(quick_start_path)],
                cwd=hypnodyne_suite_directory,
            )

            if verify_hypnodyne_processes():
                logger.info(
                    "Hypnodyne QuickStart started successfully", pid=process.pid
                )
                return process

            raise RuntimeError("Failed to start all required Hypnodyne processes")

        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                sleep(retry_delay)
            else:
                raise RuntimeError(
                    f"Failed to start QuickStart after {max_retries} attempts: {e}"
                ) from e
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] in HYPNODYNE_PROCESSES:
            proc.terminate()
            proc.wait(settings["process_termination_timeout"])
            logger.info(f"Terminated {proc.info['name']} with PID {proc.pid}")


@dataclass
class DataTypeConfig:
    buffer_position: int
    scale_function: Callable | None = None

    def get_value(self, buffer: str) -> int | float:
        value = get_word_at(buffer, self.buffer_position)
        return self.scale_function(value) if self.scale_function else value
