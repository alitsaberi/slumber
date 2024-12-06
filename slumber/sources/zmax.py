import socket
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from time import sleep

import numpy as np
from loguru import logger

from slumber import settings

_PACKET_TYPE_POSITION = 0
_VALID_PACKET_TYPES = range(1, 12)
_EXPECTED_DATA_LENGTH = 119
_SEND_BYTES_COMMAND = "LIVEMODE_SENDBYTES"
_STIMULATION_RETRIES = 15
_STIMULATION_RETRY_DELAY = 111  # Milliseconds
_STIMULATION_FLASH_LED_COMMAND = 4
_STIMULATION_PWM_MAX = 254  # 100% intensity
_STIMULATION_MAX_REPETITIONS = 127
_STIMULATION_MIN_REPETITIONS = 1
_STIMULATION_MIN_DURATION = 1
_STIMULATION_MAX_DURATION = 255
SAMPLE_RATE = 256


class LEDColor(Enum):
    RED = (2, 0, 0)
    YELLOW = (2, 2, 0)
    GREEN = (0, 2, 0)
    CYAN = (0, 2, 2)
    BLUE = (0, 0, 2)
    PURPLE = (2, 0, 2)
    WHITE = (2, 2, 2)
    OFF = (0, 0, 0)


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


def _dec2hex(decimal: int, pad: int = 2) -> str:
    """Convert decimal to hexadecimal string with padding."""
    return format(decimal, f"0{pad}x").upper()


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

    def __str__(self) -> str:
        return self.name


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
        self._message_counter = 0

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
                    logger.error(f"Failed to connect after {retry_attempts} attempts.")
                    raise ConnectionError(
                        f"Unable to connect to ZMax at {self._ip}:{self._port}"
                    ) from e
                logger.warning(f"Attempt {attempt + 1}/{retry_attempts} failed: {e}")
                sleep(retry_delay)

    def is_connected(self) -> bool:
        try:
            # Check if socket exists and is connected by attempting to get peer name
            self._socket.getpeername()
            return True
        except (OSError, AttributeError):
            return False

    def read(self, data_types: list[DataType] | None = None) -> np.ndarray:
        while True:
            message = self._receive_line_buffer()  # Raw data received

            if message.startswith("DEBUG"):  # Ignore debugging messages from the server
                logger.debug(f"Ignoring debug message: {message}")
                continue

            if not message.startswith("D"):  # Only process valid data packets
                logger.debug(f"Ignoring non-data message: {message}")
                continue

            # Split the raw data into data packets
            data_packet = message.split(".")

            if len(data_packet) != 2:
                logger.debug(f"Ignoring invalid data packet: {data_packet}")
                continue

            # Process the second part of the data packet
            data = data_packet[1]
            if not self._is_valid_data(data):
                continue

            data_types = data_types or list(DataType)
            return np.array(
                [data_type.value.get_value(data) for data_type in data_types]
            )

    def _receive_line_buffer(self):
        buffer = bytearray()
        while True:
            char = self._socket.recv(1)
            if not char:
                raise ConnectionError("Lost connection to ZMax")

            if char == b"\r":
                continue

            if char == b"\n":
                break

            buffer.extend(char)
        return buffer.decode("utf-8")

    def _is_valid_data(self, data: str) -> bool:
        """Validate the received data."""
        packet_type = get_byte_at(data, _PACKET_TYPE_POSITION)
        if packet_type not in _VALID_PACKET_TYPES:
            logger.debug(f"Ignoring invalid packet type: {packet_type}")
            return False

        if len(data) != _EXPECTED_DATA_LENGTH:
            logger.debug(f"Ignoring invalid data length: {len(data)}")
            return False

        return True

    def vibrate(
        self, on_duration: int = 10, off_duration: int = 10, repetitions: int = 1
    ) -> None:
        self.stimulate(
            led_color=LEDColor.OFF,
            on_duration=on_duration,
            off_duration=off_duration,
            repetitions=repetitions,
            vibration=True,
        )

    def stimulate(
        self,
        led_color: LEDColor = LEDColor.WHITE,
        led_intensity: int = 100,
        on_duration: int = 10,  # 10 units = 1000 ms
        off_duration: int = 10,  # 10 units = 1000 ms
        repetitions: int = 5,
        vibration: bool = True,
        alternate_eyes: bool = False,
    ) -> None:
        """
        Send stimulation pattern to ZMax device.
        The pattern is first on for on_duration, then off for off_duration.
        When alternate_eyes is True, each repetition alternates between the two LEDs.
        To turn off the LED, set led_color to LEDColor.OFF.

        Args:
            led_color (LEDColor): Color of the LED.
            led_intensity (int): Intensity of the LED in percent.
            on_duration (int): Duration of the LED on in 100 ms. (e.g. 10 = 1000ms)
            off_duration (int): Duration of the LED off in 100 ms. (e.g. 10 = 1000ms)
            repetitions (int): Number of repetitions.
            vibration (bool): Whether to vibrate.
            alternate_eyes (bool): Whether to alternate between the two LEDs.
        """

        if not (
            _STIMULATION_MIN_REPETITIONS <= repetitions <= _STIMULATION_MAX_REPETITIONS
        ):
            raise ValueError(
                f"Repetitions must be between {_STIMULATION_MIN_REPETITIONS}"
                f" and {_STIMULATION_MAX_REPETITIONS}"
            )

        if not (_STIMULATION_MIN_DURATION <= on_duration <= _STIMULATION_MAX_DURATION):
            raise ValueError(
                f"On duration must be between {_STIMULATION_MIN_DURATION}"
                f" and {_STIMULATION_MAX_DURATION}"
            )

        if not (_STIMULATION_MIN_DURATION <= off_duration <= _STIMULATION_MAX_DURATION):
            raise ValueError(
                f"Off duration must be between {_STIMULATION_MIN_DURATION}"
                f" and {_STIMULATION_MAX_DURATION}"
            )

        if not (1 <= led_intensity <= 100):
            raise ValueError("LED intensity must be between 1 to 100")

        led_intensity = int(led_intensity / 100 * _STIMULATION_PWM_MAX)

        hex_values = [
            _dec2hex(x)
            for x in [
                _STIMULATION_FLASH_LED_COMMAND,
                *led_color.value,  # Left eye
                *led_color.value,  # Right eye
                led_intensity,
                0,  # Reserved value that can affect LED color
                on_duration,
                off_duration,
                repetitions,
                int(vibration),
                int(alternate_eyes),
            ]
        ]

        command = (
            f"{_SEND_BYTES_COMMAND} {_STIMULATION_RETRIES}"
            f" {self._get_next_message_number()} {_STIMULATION_RETRY_DELAY}"
            f" {'-'.join(hex_values)}\r\n"
        )
        logger.debug(f"ZMax stimulation command: {command}")

        self.send_string(command)

    def send_string(self, message: str) -> None:
        self._socket.sendall(message.encode("utf-8"))

    def _get_next_message_number(self) -> int:
        """Get next message sequence number (0-255)"""
        self._message_counter = (self._message_counter + 1) % 256
        return self._message_counter
