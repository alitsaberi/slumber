import asyncio
import time
from collections.abc import AsyncGenerator
from enum import Enum
from multiprocessing.connection import Connection
from typing import Annotated

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import BeforeValidator, Field

from slumber import settings
from slumber.dag.units.event_logger import Event as LogEvent
from slumber.dag.units.zmax import ZMaxStimulationSignal
from slumber.dag.utils import PydanticSettings
from slumber.utils.data import Data, Event
from slumber.utils.helpers import create_enum_by_name_resolver

_CONNECTION_CHECK_INTERVAL = 0.5


class EventType(Enum):
    EYE_MOVEMENT = "eye_movement"
    AROUSAL = "arousal"
    VISUAL_CUE = "visual_cue"
    AUDITORY_CUE = "auditory_cue"
    TACTILE_CUE = "tactile_cue"
    EXPERIMENT_STATE_CHANGED = "experiment_state_changed"


class ExperimentState(Enum):
    AWAKE = "awake"
    ASLEEP = "asleep"
    WAKING = "waking"


class Settings(PydanticSettings):
    wake_up_signal: ZMaxStimulationSignal
    cueing_enabled: bool
    rem_confidence_threshold: float = Field(ge=0.0, le=1.0)
    accepted_eye_signals: list[str] = Field(default_factory=list, min_length=1)
    wake_up_signal_interval: float = Field(ge=0.0)
    experiment_state: Annotated[
        ExperimentState, BeforeValidator(create_enum_by_name_resolver(ExperimentState))
    ] = ExperimentState.AWAKE
    gui_connection: Connection | None = None
    minimum_elapsed_time: float = Field(0.0, ge=0.0)


class State(ez.State):
    start_time: float
    experiment_state: ExperimentState
    in_rem: bool  # by sleep staging
    aroused: bool
    eye_signaling: bool
    rem_cueing: bool
    gui_connection: Connection


class Master(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT_SLEEP_SCORES = ez.InputStream(Data)
    INPUT_EYE_MOVEMENT_EVENTS = ez.InputStream(list[Event])
    INPUT_AROUSAL_EVENTS = ez.InputStream(list[Event])
    INPUT_EXPERIMENT_STATE = ez.InputStream(ExperimentState)

    OUTPUT_CUEING_ENABLE_SIGNAL = ez.OutputStream(bool)
    OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)
    OUTPUT_CUEING_DECREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)
    OUTPUT_LOG_EVENT = ez.OutputStream(LogEvent)
    OUTPUT_WAKE_UP_SIGNAL = ez.OutputStream(ZMaxStimulationSignal)

    async def initialize(self) -> None:
        self.STATE.start_time = time.time()
        self.STATE.experiment_state = self.SETTINGS.experiment_state
        self.STATE.in_rem = False
        self.STATE.aroused = False
        self.STATE.eye_signaling = False
        self.STATE.rem_cueing = self.SETTINGS.cueing_enabled
        self.STATE.gui_connection = self.SETTINGS.gui_connection

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.STATE.start_time

    @ez.publisher(OUTPUT_LOG_EVENT)
    async def update_experiment_state(self) -> AsyncGenerator:
        if self.STATE.gui_connection is None:
            logger.warning(
                "GUI connection is not set. Skipping experiment state update."
            )
            return

        while True:
            if not self.STATE.gui_connection.poll():
                await asyncio.sleep(_CONNECTION_CHECK_INTERVAL)
                continue

            state = self.STATE.gui_connection.recv()
            logger.info(
                f"Updating experiment state from {self.STATE.experiment_state}"
                f" to {state}."
            )
            self.STATE.experiment_state = state
            yield (
                self.OUTPUT_LOG_EVENT,
                LogEvent(
                    type=EventType.EXPERIMENT_STATE_CHANGED,
                    new_state=self.STATE.experiment_state,
                ),
            )

    @ez.subscriber(INPUT_SLEEP_SCORES)
    @ez.publisher(OUTPUT_WAKE_UP_SIGNAL)
    @ez.publisher(OUTPUT_CUEING_ENABLE_SIGNAL)
    @ez.publisher(OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    @ez.publisher(OUTPUT_LOG_EVENT)
    async def update_in_rem(self, scores: Data) -> AsyncGenerator:
        if self.STATE.experiment_state != ExperimentState.ASLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring sleep scores.",
                experiment_state=self.STATE.experiment_state,
            )
            return

        if self.elapsed_time < self.SETTINGS.minimum_elapsed_time:
            logger.debug(
                "Minimum elapsed time not reached. Ignoring sleep scores.",
                elapsed_time=self.elapsed_time,
            )
            return

        rem_confidence = np.mean(
            scores[:, settings["sleep_scoring"]["labels"]["rem"]].array
        )
        logger.debug(f"REM confidence: {rem_confidence}")
        in_rem = rem_confidence >= self.SETTINGS.rem_confidence_threshold

        if not in_rem and self.STATE.in_rem:
            logger.info("Participant is no longer in REM. Waking up participant...")
            async for signal in self._wake_up():
                yield signal
        elif in_rem and not self.STATE.in_rem and self.STATE.rem_cueing:
            logger.info("Participant is now in REM. Enabling cueing...")
            yield (self.OUTPUT_CUEING_ENABLE_SIGNAL, True)
            yield (self.OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, True)

        self.STATE.in_rem = in_rem

    @ez.subscriber(INPUT_EYE_MOVEMENT_EVENTS)
    @ez.publisher(OUTPUT_WAKE_UP_SIGNAL)
    @ez.publisher(OUTPUT_CUEING_ENABLE_SIGNAL)
    @ez.publisher(OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    @ez.publisher(OUTPUT_LOG_EVENT)
    async def update_eye_signaling(self, events: list[Event]) -> AsyncGenerator:
        async for output_event in self._log_events(events, EventType.EYE_MOVEMENT):
            yield output_event

        if self.STATE.experiment_state != ExperimentState.ASLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring eye movement events.",
                experiment_state=self.STATE.experiment_state,
            )
            return

        if self.elapsed_time < self.SETTINGS.minimum_elapsed_time:
            logger.debug(
                "Minimum elapsed time not reached. Ignoring eye movement events.",
                elapsed_time=self.elapsed_time,
            )
            return

        logger.debug(f"Eye signals: {events}")
        eye_signaling = any(
            event.label.startswith(prefix)
            for event in events
            for prefix in self.SETTINGS.accepted_eye_signals
        )

        if not eye_signaling and self.STATE.eye_signaling and not self.STATE.in_rem:
            logger.info("Eye signaling stopped in non rem. Waking up participant...")
            async for signal in self._wake_up():
                yield signal
        elif eye_signaling and not self.STATE.eye_signaling and self.STATE.in_rem:
            logger.info(
                "Eye signaling started. Stopping increasing cueing intensity..."
            )
            yield (self.OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)

        self.STATE.eye_signaling = eye_signaling

    @ez.subscriber(INPUT_AROUSAL_EVENTS)
    @ez.publisher(OUTPUT_CUEING_ENABLE_SIGNAL)
    @ez.publisher(OUTPUT_CUEING_DECREASE_INTENSITY_SIGNAL)
    async def update_aroused(self, events: list[Event]) -> AsyncGenerator:
        async for output_event in self._log_events(
            events, EventType.AROUSAL, include_label=False
        ):
            yield output_event

        if self.STATE.experiment_state != ExperimentState.ASLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring arousal events.",
                experiment_state=self.STATE.experiment_state,
            )
            return

        if self.elapsed_time < self.SETTINGS.minimum_elapsed_time:
            logger.debug(
                "Minimum elapsed time not reached. Ignoring arousal events.",
                elapsed_time=self.elapsed_time,
            )
            return

        logger.debug(f"Arousal events: {events}")
        aroused = bool(events)

        if (
            aroused
            and not self.STATE.aroused
            and self.STATE.in_rem
            and self.STATE.rem_cueing
        ):
            logger.info("Participant is aroused in REM. Disabling cueing...")
            yield (self.OUTPUT_CUEING_ENABLE_SIGNAL, False)
            yield (self.OUTPUT_CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)
            yield (self.OUTPUT_CUEING_DECREASE_INTENSITY_SIGNAL, False)
        elif (
            not aroused
            and self.STATE.aroused
            and self.STATE.in_rem
            and self.STATE.rem_cueing
        ):
            logger.info("Participant is no longer aroused in REM. Enabling cueing...")
            yield (self.OUTPUT_CUEING_ENABLE_SIGNAL, True)

        self.STATE.aroused = aroused

    async def _wake_up(self) -> AsyncGenerator:
        self.STATE.experiment_state = ExperimentState.WAKING
        yield (
            self.OUTPUT_LOG_EVENT,
            LogEvent(
                type=EventType.EXPERIMENT_STATE_CHANGED,
                new_state=self.STATE.experiment_state,
            ),
        )
        yield (self.OUTPUT_CUEING_ENABLE_SIGNAL, False)

        while self.STATE.experiment_state != ExperimentState.AWAKE:
            yield (self.OUTPUT_WAKE_UP_SIGNAL, self.SETTINGS.wake_up_signal)
            logger.info("Wake up signal sent", signal=self.SETTINGS.wake_up_signal)
            await asyncio.sleep(self.SETTINGS.wake_up_signal_interval)

    async def _log_events(
        self, events: list[Event], event_type: EventType, include_label: bool = True
    ) -> AsyncGenerator:
        for event in events:
            yield (
                self.OUTPUT_LOG_EVENT,
                LogEvent(
                    type=event_type,
                    timestamp=event.start_time,
                    duration=event.end_time - event.start_time,
                    label=event.label if include_label else None,
                ),
            )
