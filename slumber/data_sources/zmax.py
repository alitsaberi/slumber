import socket
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from time import sleep

import numpy as np
from loguru import logger

from slumber import settings

_PACKET_TYPE_BUFFER_POSITION = 0
_VALID_PACKET_TYPES = range(1, 12)
_EXPECTED_BUFFER_LENGTH = 119
SAMPLE_RATE = 256


def get_word_at(buffer: str, index: int) -> int:
    return get_byte_at(buffer, index) * 256 + get_byte_at(buffer, index + 1)


def get_byte_at(buffer: str, index: int) -> int:
    hex_str = buffer[index * 3 : index * 3 + 2]
    return int(hex_str, 16)


def _scale_eeg(value: int) -> float:
    """
    Convert the raw EEG value to uV.
    """
    uv_range = 3952
    return ((value - 32768) * uv_range) / 65536


def _scale_accelerometer(value: int) -> float:
    """
    Convert the raw accelerometer value to 'g'.
    """
    return value * 4 / 4096 - 2


def _scale_battery(value: int) -> float:
    """
    Convert the raw battery voltage value to volts.
    """
    return value / 1024 * 6.60


def _scale_body_temperature(value: int) -> float:
    """
    Convert the raw body temperature value to Celsius.
    """
    return 15 + ((value / 1024 * 3.3 - 1.0446) / 0.0565537333333333)


@dataclass
class DataTypeConfig:
    buffer_position: int
    scale_function: Callable | None = None

    def get_value(self, buffer: str) -> int | float:
        value = get_word_at(buffer, self.buffer_position)
        return self.scale_function(value) if self.scale_function else value


class DataType(Enum):
    EEG_RIGHT = DataTypeConfig(1, _scale_eeg)
    EEG_LEFT = DataTypeConfig(3, _scale_eeg)
    ACCELEROMETER_X = DataTypeConfig(5, _scale_accelerometer)
    ACCELEROMETER_Y = DataTypeConfig(7, _scale_accelerometer)
    ACCELEROMETER_Z = DataTypeConfig(9, _scale_accelerometer)
    BODY_TEMP = DataTypeConfig(36, _scale_body_temperature)
    BATTERY = DataTypeConfig(23, _scale_battery)
    NOISE = DataTypeConfig(19)
    LIGHT = DataTypeConfig(21)
    NASAL_LEFT = DataTypeConfig(11)
    NASAL_RIGHT = DataTypeConfig(13)
    OXIMETER_INFRARED_AC = DataTypeConfig(27)
    OXIMETER_RED_AC = DataTypeConfig(25)
    OXIMETER_DARK_AC = DataTypeConfig(34)
    OXIMETER_INFRARED_DC = DataTypeConfig(17)
    OXIMETER_RED_DC = DataTypeConfig(15)
    OXIMETER_DARK_DC = DataTypeConfig(32)


class ZMax:
    def __init__(
        self,
        ip: str,
        port: int,
        socket_timeout: int = settings["zmax"]["socket_timeout"],
    ) -> None:
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(socket_timeout)

    def __enter__(self) -> "ZMax":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        if self._socket:
            self._socket.close()

    def connect(
        self,
        retry_attempts: int = settings["zmax"]["retry_attempts"],
        retry_delay: int = settings["zmax"]["retry_delay"],
    ) -> None:
        for attempt in range(retry_attempts):
            try:
                self._socket.connect((self._ip, self._port))
                self.send_string("HELLO\n")  # ?
                logger.info(f"Connected to ZMax at {self._ip}:{self._port}")
                return
            except OSError as e:
                if attempt == retry_attempts - 1:
                    logger.error(
                        "Failed to connect to ZMax after"
                        f" {retry_attempts} attempts: {e}"
                    )
                    raise ConnectionError(
                        f"Unable to connect to ZMax at {self._ip}:{self._port}"
                    ) from None
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                sleep(retry_delay)

    def is_connnected(self) -> bool:
        try:
            # Check if socket exists and is connected by attempting to get peer name
            self._socket.getpeername()
            return True
        except (OSError, AttributeError):
            return False

    def read(self, data_types: list[DataType] | None = None) -> np.ndarray:
        while True:
            buffer = self._receive_line_buffer()

            if str.startswith(buffer, "DEBUG"):  # ignore debugging messages from server
                logger.debug(f"Ignoring debug message: {buffer}")
                continue

            if not str.startswith(buffer, "D"):  # only process data packets
                logger.debug(f"Ignoring message: {buffer}")
                continue

            packet = buffer.split(".")

            if len(packet) != 2:
                logger.debug(f"Ignoring invalid packet: {buffer}")
                continue

            buffer = packet[1]
            packet_type = get_byte_at(buffer, _PACKET_TYPE_BUFFER_POSITION)

            if packet_type not in _VALID_PACKET_TYPES:
                logger.debug(
                    f"Ignoring invalid packet with type {packet_type}: {buffer}"
                )
                continue

            if len(buffer) != _EXPECTED_BUFFER_LENGTH:
                logger.debug(
                    f"Ignoring invalid packet with length {len(buffer)}: {buffer}"
                )
                continue

            data_types = data_types or list(DataType)
            return np.array(
                [data_type.value.get_value(buffer) for data_type in data_types]
            )

    def send_string(self, message: str) -> None:
        self._socket.sendall(message.encode("utf-8"))

    def _receive_line_buffer(self):
        buffer = bytearray()
        while True:
            char = self._socket.recv(1)
            if not char:
                raise ConnectionError("Connection with ZMax lost")

            if char == b"\r":
                continue

            if char == b"\n":
                break

            buffer.extend(char)
        return buffer.decode("utf-8")
