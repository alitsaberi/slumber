import socket
import types
from time import sleep

import numpy as np
from loguru import logger

from .constants import (
    DEFAULTS,
    DONGLE_MESSAGE_PREFIX,
    EXPECTED_DATA_LENGTH,
    LED_MAX_INTENSITY,
    LED_MIN_INTENSITY,
    LIVEMODE_SENDBYTES_COMMAND,
    PACKET_TYPE_POSITION,
    SENDBYTES_MAX_RETRIES,
    STIMULATION_FLASH_LED_COMMAND,
    STIMULATION_MAX_DURATION,
    STIMULATION_MAX_REPETITIONS,
    STIMULATION_MIN_DURATION,
    STIMULATION_MIN_REPETITIONS,
    STIMULATION_PWM_MAX,
    STIMULATION_RETRY_DELAY,
    VALID_PACKET_TYPES,
)
from .enums import DataType, DongleStatus, LEDColor
from .exceptions import ConnectionClosedError
from .utils import dec2hex, get_byte_at


def _initialize_socket(
    socket_timeout: float | None = None,
) -> socket.socket:
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.settimeout(socket_timeout)
    return _socket


def _is_dongle_message(message: str) -> bool:
    return message.startswith(DONGLE_MESSAGE_PREFIX)


class ZMax:
    def __init__(
        self,
        ip: str = DEFAULTS["ip"],
        port: int = DEFAULTS["port"],
        socket_timeout: float | None = DEFAULTS["socket_timeout"],
    ) -> None:
        self._ip = ip
        self._port = port
        self._socket_timeout = socket_timeout
        self._socket = _initialize_socket(self._socket_timeout)
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

        self._socket = _initialize_socket(self._socket_timeout)

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
                self.send_string("HELLO\n")
                return
            except OSError as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{retry_attempts} to connect to {self!r}"
                    f" failed: {e}"
                )
                sleep(retry_delay)

        raise ConnectionError(
            f"Failed to connect to {self!r} after {retry_attempts} attempts"
        )

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
        self._dongle_status = DongleStatus[message.split("_")[2]]
        logger.info(f"Dongle status: {self._dongle_status.value}")

    def read(self, data_types: list[DataType] | None = None) -> np.ndarray:
        while True:
            message = self._receive_line()

            if message.startswith("DEBUG"):  # Ignore debugging messages from the server
                logger.debug(f"Debug message: {message}")
                continue

            if _is_dongle_message(message):
                logger.debug(f"Dongle message: {message}")
                self._handle_dongle_message(message)
                continue

            if not message.startswith("D"):  # Only process valid data packets
                logger.debug(f"Non-data message: {message}")
                continue

            try:
                _, data = message.split(".")
            except ValueError as e:
                logger.warning(
                    f"Failed to extract data from data message {message}: {e}"
                )
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
                raise ConnectionClosedError("The connection was closed by the server.")

            if char == b"\r":
                continue

            if char == b"\n":
                break

            line.extend(char)
        return line.decode("utf-8")

    def _is_valid_data(self, data: str) -> bool:
        """Validate the received data"""
        packet_type = get_byte_at(data, PACKET_TYPE_POSITION)
        if packet_type not in VALID_PACKET_TYPES:
            logger.warning(f"Invalid type: {packet_type}")
            return False

        if len(data) != EXPECTED_DATA_LENGTH:
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

        led_intensity = int(led_intensity / 100 * STIMULATION_PWM_MAX)

        hex_values = [
            dec2hex(x)
            for x in [
                STIMULATION_FLASH_LED_COMMAND,
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
            f"{LIVEMODE_SENDBYTES_COMMAND} {SENDBYTES_MAX_RETRIES}"
            f" {self._get_next_live_sequence_number()} {STIMULATION_RETRY_DELAY}"
            f" {'-'.join(hex_values)}\r\n"
        )
        logger.debug(f"ZMax stimulation command: {command}")

        self.send_string(command)

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
