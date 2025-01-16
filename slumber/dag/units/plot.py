from datetime import datetime

import ezmsg.core as ez
from loguru import logger
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz

from slumber.dag.utils import PydanticSettings
from slumber.utils.data import (
    TimestampedArray,
)


class Settings(PydanticSettings):
    figure_size: tuple[int, int] = (12, 8)


class State(ez.State):
    figure: plt.Figure
    ax = plt.Axes


class Plot(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT = ez.InputStream(TimestampedArray)

    async def initialize(self):
        plt.ioff()

        self.STATE.figure, self.STATE.ax = plt.subplots(
            figsize=self.SETTINGS.figure_size
        )
        self.STATE.ax.set_xlabel("Time (s)")
        self.STATE.ax.set_ylabel("Amplitude")
        self.STATE.ax.grid(True)

        # Configure the x-axis for datetime
        self.STATE.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        self.STATE.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        self.STATE.figure.show()

    @ez.subscriber(INPUT)
    async def update_figure(self, message: TimestampedArray) -> None:
        plt.figure(self.STATE.figure.number)
        logger.debug(f"Plotting {message}.")
        
        cet = pytz.timezone("Europe/Berlin")
        times = [
            datetime.fromtimestamp(ts, tz=pytz.utc).astimezone(cet)
            for ts in message.timestamps
        ]

        self.STATE.ax.clear()
        self.STATE.ax.set_xlabel("Time (s)")
        self.STATE.ax.set_ylabel("Amplitude")
        self.STATE.ax.grid(True)

        for i, channel in enumerate(message.channel_names):
            self.STATE.ax.plot(times, message.array[:, i], label=channel, linewidth=0.5)

        self.STATE.ax.legend()

        self.STATE.figure.canvas.draw()
        self.STATE.figure.canvas.flush_events()
