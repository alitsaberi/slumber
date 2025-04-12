from enum import Enum

from .utils import (
    DataTypeConfig,
    scale_accelerometer,
    scale_battery,
    scale_body_temperature,
    scale_eeg,
)


class DongleStatus(Enum):
    UNKNOWN = "unknown"
    INSERTED = "inserted"
    REMOVED = "removed"


class LEDColor(Enum):
    RED = (2, 0, 0)
    YELLOW = (2, 2, 0)
    GREEN = (0, 2, 0)
    CYAN = (0, 2, 2)
    BLUE = (0, 0, 2)
    PURPLE = (2, 0, 2)
    WHITE = (2, 2, 2)
    OFF = (0, 0, 0)


class DataType(Enum):
    EEG_RIGHT = DataTypeConfig(1, scale_eeg)
    EEG_LEFT = DataTypeConfig(3, scale_eeg)
    ACCELEROMETER_X = DataTypeConfig(5, scale_accelerometer)
    ACCELEROMETER_Y = DataTypeConfig(7, scale_accelerometer)
    ACCELEROMETER_Z = DataTypeConfig(9, scale_accelerometer)
    BODY_TEMP = DataTypeConfig(36, scale_body_temperature)
    BATTERY = DataTypeConfig(23, scale_battery)
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
