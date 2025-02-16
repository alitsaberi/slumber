import socket
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from subprocess import Popen
from time import sleep
import types

import numpy as np
import psutil
from loguru import logger

from slumber import settings


class Mode(Enum):
    """
    Enum representing the different modes of operation for the ZMax device.
    """

    LIVE = "LIVEMODE"
    IDLE = "IDLEMODE"


class Command(Enum):
    """
    Enum representing the different commands that can be sent to the
    """

    SEND_BYTES = "SENDBYTES"
    
class DongleStatus(Enum):
    UNKNOWN = "unknown"
    INSERTED = "inserted"
    REMOVED = "removed"


_DONGLE_MESSAGE_PREFIX = "_DONGLE"
_SENDBYTES_MAX_RETRIES = 1
_PACKET_TYPE_POSITION = 0
_VALID_PACKET_TYPES = range(1, 12)
_EXPECTED_DATA_LENGTH = 119

_STIMULATION_RETRY_DELAY = 111  # Milliseconds
_STIMULATION_FLASH_LED_COMMAND = 4
_STIMULATION_PWM_MAX = 254  # 100% intensity
STIMULATION_MAX_REPETITIONS = 127
STIMULATION_MIN_REPETITIONS = 1
STIMULATION_MIN_DURATION = 1
STIMULATION_MAX_DURATION = 255
LED_MIN_INTENSITY = 1
LED_MAX_INTENSITY = 100
SAMPLE_RATE = 256
MIN_VOLTAGE = 3.12
MAX_VOLTAGE = 4.2


DEFAULTS = settings["zmax"]
HDSERVER_APP_NAME = "HDServer.exe"


class ConnectionClosedError(Exception):
    pass


class HDServerAlreadyRunningError(Exception):
    pass


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


def open_server(log_file_path: Path | None = None) -> Popen:
    """
    Opens the Hypnodyne HDServer application.

    Args:
        log_file_path: Optional path to write server logs to

    Returns:
        Popen: Process handle for the server

    Raises:
        FileNotFoundError: If HDServer executable not found
        HDServerAlreadyRunningError: If server is already running
        RuntimeError: If server fails to start
    """
    hypnodyne_suite_directory = Path(DEFAULTS["hypnodyne_suite_directory"])
    hdserver_path = hypnodyne_suite_directory / HDSERVER_APP_NAME

    # Validate server executable exists
    if not hdserver_path.exists():
        raise FileNotFoundError(f"HDServer executable not found at {hdserver_path}")

    # Check if server already running
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == HDSERVER_APP_NAME:
            raise HDServerAlreadyRunningError(
                f"HDServer is already running as PID {proc.pid}"
            )

    stdout = open(log_file_path, "w") if log_file_path else None  # noqa: SIM115

    try:
        process = Popen(
            [str(hdserver_path)], cwd=hypnodyne_suite_directory, stdout=stdout
        )
        logger.info("Hypnodyne HDServer started", path=hdserver_path, pid=process.pid)
        return process
    except Exception as e:
        if stdout:
            stdout.close()
        raise RuntimeError(f"Failed to start HDServer: {e}") from e


def voltage_to_percentage(voltage: float) -> int:
    voltage = max(MIN_VOLTAGE, min(voltage, MAX_VOLTAGE))
    percentage = ((voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE)) * 100
    return round(percentage)


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

    @property
    def category(self) -> str:
        return self.name.split("_")[0]

    @classmethod
    def get_by_category(cls, category: str) -> list["DataType"]:
        return [data_type for data_type in cls if data_type.category == category]


def _initialize_socket(
    socket_timeout: float | None = None,
) -> socket.socket:
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.settimeout(socket_timeout)
    return _socket


def _is_dongle_message(message: str) -> bool:
    return message.startswith(_DONGLE_MESSAGE_PREFIX)

class ZMax:
    def __init__(
        self,
        ip: str = DEFAULTS["ip"],
        port: int = DEFAULTS["port"],
        socket_timeout: float | None = DEFAULTS["socket_timeout"],
    ) -> None:
        self._ip = ip
        self._port = port
        self._socket = _initialize_socket(socket_timeout)
        self._idle_sequence_number = 1
        self._live_sequence_number = 1
        self._dongle_status = DongleStatus.UNKNOWN

    def __repr__(self) -> str:
        return f"ZMax(ip={self._ip}, port={self._port})"

    def __enter__(self) -> "ZMax":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        self.disconnect()

    def disconnect(self) -> None:
        if self._socket:
            self._socket.close()
            logger.info(f"Closed connection to {self!r}")

    def connect(
        self,
        retry_attempts: int = DEFAULTS["retry_attempts"],
        retry_delay: float = DEFAULTS["retry_delay"],
    ) -> None:
        if self.is_connected():
            logger.warning(f"Already connected to {self!r}")
            return

        for attempt in range(retry_attempts):
            try:
                self._socket.connect((self._ip, self._port))
                logger.info(f"Connected to {self!r}")
                self._handle_handshake()
            except OSError as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{retry_attempts} to connect to {self!r}"
                    f" failed: {e}"
                )
                sleep(retry_delay)

        raise ConnectionError(
            f"Failed to connect to {self!r} after {retry_attempts} attempts"
        )
        
    def _handle_handshake(self) -> None:
        # Expect 3 lines: version, dongle status, RF channel
        logger.info("Handling handshake...")
        for _ in range(3):  # Expect 3 lines
            message = self._receive_line()
            
            if _is_dongle_message(message):
                self._handle_dongle_message(message)
                
    @property
    def dongle_inserted(self) -> bool:
        return self._dongle_status == DongleStatus.INSERTED

    def is_connected(self) -> bool:
        try:
            self._socket.getpeername()
            return True
        except OSError:
            return False
        
    def _handle_dongle_message(self, message: str) -> None:
        self._dongle_status = DongleStatus(message.split("_")[2])
        logger.info(f"Dongle status: {self._dongle_status.value}")

    def read_with_keepalive(
        self, data_types: list[DataType] | None = None
    ) -> np.ndarray:
        while True:
            try:
                return self.read(data_types)
            except TimeoutError:
                logger.debug("Timeout while reading data from the server")
                self.send_idle_command()

    def read(self, data_types: list[DataType] | None = None) -> np.ndarray:
        while True:
            message = self._receive_line()

            if message.startswith("DEBUG"):  # Ignore debugging messages from the server
                logger.debug(f"Debug message: {message}")
                continue

            if not message.startswith("D"):  # Only process valid data packets
                logger.debug(f"Non-data message: {message}")
                continue
            
            if not _is_dongle_message(message):
                logger.debug("Dongle message: {message}")
                self._handle_dongle_message(message)
                continue
            
            try:
                _, data = message.split(".")
            except ValueError as e:
                logger.warning(f"Failed to extract data from data message {message}: {e}")
                continue
            
            if not self._is_valid_data(data):
                continue

            data_types = data_types or list(DataType)
            return np.array(
                [data_type.value.get_value(data) for data_type in data_types]
            )

    def _receive_line(self) -> str:
        line = bytearray()
        while True:
            char = self._socket.recv(1)
            if not char:
                raise ConnectionClosedError(
                    "The connection was closed by the server."
                    " Make sure the server is running."
                )

            if char == b"\r":
                continue

            if char == b"\n":
                break

            line.extend(char)
        return line.decode("utf-8")

    def _is_valid_data(self, data: str) -> bool:
        """Validate the received data"""
        packet_type = get_byte_at(data, _PACKET_TYPE_POSITION)
        if packet_type not in _VALID_PACKET_TYPES:
            logger.warning(f"Invalid type: {packet_type}")
            return False

        if len(data) != _EXPECTED_DATA_LENGTH:
            logger.warning(f"Invalid data length: {len(data)}")
            return False

        return True

    def vibrate(
        self,
        on_duration: int,
        off_duration: int,
        repetitions: int,
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
        led_color: LEDColor,
        on_duration: int,  # 10 units = 1000 ms
        off_duration: int,  # 10 units = 1000 ms
        repetitions: int,
        vibration: bool,
        led_intensity: int = LED_MAX_INTENSITY,
        alternate_eyes: bool = False,
    ) -> None:
        """
        Send stimulation pattern to ZMax device.
        The pattern is first on for on_duration, then off for off_duration.
        When alternate_eyes is True, each repetition alternates between the two LEDs.
        To turn off the LED, set led_color to LEDColor.OFF.

        Args:
            led_color (LEDColor): Color of the LED.
            on_duration (int): Duration of the LED on in 100 ms. (e.g. 10 = 1000ms)
            off_duration (int): Duration of the LED off in 100 ms. (e.g. 10 = 1000ms)
            repetitions (int): Number of repetitions.
            vibration (bool): Whether to vibrate.
            led_intensity (int): Intensity of the LED in percent. Defaults to 100.
            alternate_eyes (bool): Whether to alternate between the two LEDs.
                Defaults to False.
        """

        if not (
            STIMULATION_MIN_REPETITIONS <= repetitions <= STIMULATION_MAX_REPETITIONS
        ):
            raise ValueError(
                f"Repetitions must be between {STIMULATION_MIN_REPETITIONS}"
                f" and {STIMULATION_MAX_REPETITIONS}"
            )

        if not (STIMULATION_MIN_DURATION <= on_duration <= STIMULATION_MAX_DURATION):
            raise ValueError(
                f"On duration must be between {STIMULATION_MIN_DURATION}"
                f" and {STIMULATION_MAX_DURATION}"
            )

        if not (STIMULATION_MIN_DURATION <= off_duration <= STIMULATION_MAX_DURATION):
            raise ValueError(
                f"Off duration must be between {STIMULATION_MIN_DURATION}"
                f" and {STIMULATION_MAX_DURATION}"
            )

        if not (LED_MIN_INTENSITY <= led_intensity <= LED_MAX_INTENSITY):
            raise ValueError(
                f"LED intensity must be between {LED_MIN_INTENSITY}"
                f" to {LED_MIN_INTENSITY}"
            )

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
            f"{Mode.LIVE.value}_{Command.SEND_BYTES.value} {_SENDBYTES_MAX_RETRIES}"
            f" {self._get_next_live_sequence_number()} {_STIMULATION_RETRY_DELAY}"
            f" {'-'.join(hex_values)}\r\n"
        )
        logger.debug(f"ZMax stimulation command: {command}")

        self.send_string(command)
        
    def send_idle_command(self) -> None:
        self.send_string(
            f"{Mode.IDLE.value}_{Command.SEND_BYTES.value}"
            f" {_SENDBYTES_MAX_RETRIES} {self._idle_sequence_number}\n"
        )
        self._idle_sequence_number += 1

    def send_string(self, message: str) -> None:
        self._socket.sendall(message.encode("utf-8"))

    def _get_next_live_sequence_number(self) -> int:
        self._live_sequence_number += 1
        return self._live_sequence_number % 256


def is_connected(zmax: ZMax) -> ZMax:
    """
    Check if the ZMax is connected.
    Can be used in Pydantic models to validate the connection.
    """
    if not zmax.is_connected():
        raise ValueError(f"{zmax} is not connected")
    return zmax
