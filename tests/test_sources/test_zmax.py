import socket
from unittest.mock import patch

import numpy as np
import pytest

from slumber.sources.zmax import EXPECTED_DATA_LENGTH, DataType, ZMax


@pytest.fixture
def mock_socket():
    with patch("socket.socket") as mock:
        yield mock


@pytest.fixture
def zmax_device(mock_socket):
    return ZMax("127.0.0.1", 8080)


def test_zmax_initialization():
    zmax = ZMax("127.0.0.1", 8080)
    assert zmax._ip == "127.0.0.1"
    assert zmax._port == 8080


def test_zmax_context_manager(mock_socket):
    with ZMax("127.0.0.1", 8080) as zmax:
        assert zmax.is_connected()


def test_zmax_connection_error(mock_socket):
    mock_socket.return_value.connect.side_effect = OSError()
    with pytest.raises(socket.error):
        ZMax("127.0.0.1", 8080).__enter__()


def test_zmax_is_connected(zmax_device):
    zmax_device._socket.getpeername.return_value = True
    assert zmax_device.is_connected() is True

    zmax_device._socket.getpeername.side_effect = OSError()
    assert zmax_device.is_connected() is False


def test_zmax_read(zmax_device, caplog):
    debug_line = (
        b"D",
        b"E",
        b"B",
        b"U",
        b"G",
        b" ",
        b"t",
        b"e",
        b"s",
        b"t",
        b" ",
        b"m",
        b"e",
        b"s",
        b"s",
        b"a",
        b"g",
        b"e",
        b"\n",
    )

    invalid_line = (
        b"I",
        b"n",
        b"v",
        b"a",
        b"l",
        b"i",
        b"d",
        b" ",
        b"m",
        b"e",
        b"s",
        b"s",
        b"a",
        b"g",
        b"e",
        b"\n",
    )

    invalid_length_line = (b"D", b".", b"0", b"1", b"0", b"2", b"0", b"3", b"\n")
    valid_line = (
        (b"D", b".", b"0", b"1")
        + tuple(b"1" for _ in range(EXPECTED_DATA_LENGTH - 2))
        + (b"\n",)
    )
    zmax_device._socket.recv.side_effect = (
        debug_line + invalid_line + invalid_length_line + valid_line
    )
    result = zmax_device.read()
    assert "Ignoring debug message: DEBUG test message" in caplog.text
    assert "Ignoring non-data message: Invalid message" in caplog.text
    assert "Ignoring invalid data length: 6" in caplog.text
    assert isinstance(result, np.ndarray)
    assert result.shape == (len(DataType),)


def test_zmax_connection_lost(zmax_device):
    zmax_device._socket.recv.return_value = b""
    with pytest.raises(ConnectionError, match="Lost connection to ZMax"):
        zmax_device.read()


def test_data_type_scaling():
    # Test EEG scaling
    assert DataType.EEG_LEFT.value.scale_function(32768) == 0

    # Test accelerometer scaling
    assert DataType.ACCELEROMETER_X.value.scale_function(2048) == 0

    # Test battery scaling
    assert isinstance(DataType.BATTERY.value.scale_function(512), float)

    # Test body temperature scaling
    assert isinstance(DataType.BODY_TEMP.value.scale_function(512), float)
