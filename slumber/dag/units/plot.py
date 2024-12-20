import ezmsg.core as ez
import matplotlib.pyplot as plt
from loguru import logger

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import (
    TimestampedArray,
)
from slumber.utils.time import timestamp_to_datetime


class Settings(PydanticSettings):
    figure_size: tuple[int, int] = (12, 8)
    x_label: str = "Timestamp"
    y_label: str = "Amplitude"
    line_width: int = 0.5


class State(ez.State):
    figure: plt.Figure
    axes = plt.Axes


class Plot(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT = ez.InputStream(TimestampedArray)

    async def initialize(self):
        plt.ioff()

        self.STATE.figure, self.STATE.axes = plt.subplots(
            figsize=self.SETTINGS.figure_size
        )
        self._reset_axes()

        self.STATE.figure.show()

    @ez.subscriber(INPUT)
    async def update_figure(self, message: TimestampedArray) -> None:
        plt.figure(self.STATE.figure.number)
        logger.debug(f"Plotting {message}.")

        datetimes = [
            timestamp_to_datetime(timestamp) for timestamp in message.timestamps
        ]

        for i, channel in enumerate(message.channel_names):
            self.STATE.axes.plot(
                datetimes,
                message.array[:, i],
                label=channel,
                linewidth=self.SETTINGS.line_width,
            )

        self._reset_axes()

        self.STATE.axes.legend()
        self.STATE.figure.canvas.draw()
        self.STATE.figure.canvas.flush_events()

    def _reset_axes(self) -> None:
        self.STATE.axes.clear()
        self.STATE.axes.set_xlabel(self.SETTINGS.x_label)
        self.STATE.axes.set_ylabel(self.SETTINGS.y_label)
        self.STATE.axes.grid(True)
