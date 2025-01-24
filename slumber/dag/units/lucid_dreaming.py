import asyncio
import time
from collections.abc import AsyncGenerator
from enum import Enum, auto
from typing import Annotated

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import BeforeValidator, Field

from slumber import settings
from slumber.dag.units.zmax import ZMaxStimulationSignal
from slumber.dag.utils import PydanticSettings
from slumber.utils.data import Data, Event
from slumber.utils.helpers import create_enum_by_name_resolver


class ExperimentState(Enum):
    WAKE = auto()
    SLEEP = auto()
    WAKING = auto()


class Settings(PydanticSettings):
    wake_up_signal: ZMaxStimulationSignal
    cueing_enabled: bool
    rem_confidence_threshold: float = Field(ge=0.0, le=1.0)
    accepted_eye_signals: list[str] = Field(default_factory=list, min_length=1)
    wake_up_signal_interval: float = Field(ge=0.0)
    experiment_state: Annotated[
        ExperimentState, BeforeValidator(create_enum_by_name_resolver(ExperimentState))
    ] = ExperimentState.WAKE


class State(ez.State):
    start_time: float
    experiment_state: ExperimentState
    in_rem: bool  # by sleep staging
    aroused: bool
    eye_signaling: bool
    cueing_enabled: bool


class Master(ez.Unit):
    SETTINGS = Settings
    STATE = State

    SLEEP_SCORES = ez.InputStream(Data)
    EYE_MOVEMENT_EVENTS = ez.InputStream(list[Event])
    AROUSAL_EVENTS = ez.InputStream(list[Event])
    EXPERIMENT_STATE = ez.InputStream(ExperimentState)

    CUEING_ENABLE_SIGNAL = ez.OutputStream(bool)
    CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)
    CUEING_DECREASE_INTENSITY_SIGNAL = ez.OutputStream(bool)

    WAKE_UP_SIGNAL = ez.OutputStream(ZMaxStimulationSignal)

    async def initialize(self) -> None:
        self.STATE.start_time = time.time()
        self.STATE.experiment_state = self.SETTINGS.experiment_state
        self.STATE.in_rem = False
        self.STATE.aroused = False
        self.STATE.eye_signaling = False
        self.STATE.cueing_enabled = self.SETTINGS.cueing_enabled

    # @ez.publisher(CUEING_ENABLE_SIGNAL)
    # @ez.publisher(CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    # @ez.publisher(CUEING_DECREASE_INTENSITY_SIGNAL)
    # async def run(self) -> AsyncGenerator:
    #     await asyncio.sleep(5)
    #     yield (self.CUEING_ENABLE_SIGNAL, True)
    #     await asyncio.sleep(20)
    #     for _ in range(3):
    #         yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, True)
    #         await asyncio.sleep(20)
    #     yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)
    #     await asyncio.sleep(20)
    #     yield (self.CUEING_DECREASE_INTENSITY_SIGNAL, True)
    #     await asyncio.sleep(20)
    #     yield (self.CUEING_ENABLE_SIGNAL, False)
    #     await asyncio.sleep(20)
    #     raise ez.NormalTermination

    @ez.subscriber(EXPERIMENT_STATE)
    def update_experiment_state(self, state: ExperimentState) -> None:
        logger.info(
            f"Updating experiment state from {self.STATE.experiment_state} to {state}."
        )
        self.STATE.experiment_state = state

    @ez.subscriber(SLEEP_SCORES)
    @ez.publisher(WAKE_UP_SIGNAL)
    @ez.publisher(CUEING_ENABLE_SIGNAL)
    @ez.publisher(CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    async def update_in_rem(self, scores: Data) -> AsyncGenerator:
        if self.STATE.experiment_state != ExperimentState.SLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring sleep scores.",
                experiment_state=self.STATE.experiment_state,
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
        elif in_rem and not self.STATE.in_rem and self.STATE.cueing_enabled:
            logger.info("Participant is now in REM. Enabling cueing...")
            yield (self.CUEING_ENABLE_SIGNAL, True)
            yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, True)

        self.STATE.in_rem = in_rem

    @ez.subscriber(EYE_MOVEMENT_EVENTS)
    @ez.publisher(WAKE_UP_SIGNAL)
    @ez.publisher(CUEING_ENABLE_SIGNAL)
    @ez.publisher(CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL)
    async def update_eye_signaling(self, events: list[Event]) -> AsyncGenerator:
        if self.STATE.experiment_state != ExperimentState.SLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring eye movement events.",
                experiment_state=self.STATE.experiment_state,
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
            yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)

        self.STATE.eye_signaling = eye_signaling

    @ez.subscriber(AROUSAL_EVENTS)
    @ez.publisher(CUEING_ENABLE_SIGNAL)
    @ez.publisher(CUEING_DECREASE_INTENSITY_SIGNAL)
    async def update_aroused(self, events: list[Event]) -> AsyncGenerator:
        if self.STATE.experiment_state != ExperimentState.SLEEP:
            logger.debug(
                "Experiment is not in sleep state. Ignoring arousal events.",
                experiment_state=self.STATE.experiment_state,
            )
            return

        logger.debug(f"Arousal events: {events}")
        aroused = bool(events)

        if (
            aroused
            and not self.STATE.aroused
            and self.STATE.in_rem
            and self.STATE.cueing_enabled
        ):
            logger.info("Participant is aroused in REM. Disabling cueing...")
            yield (self.CUEING_ENABLE_SIGNAL, False)
            yield (self.CUEING_ENABLE_INCREASE_INTENSITY_SIGNAL, False)
            yield (self.CUEING_DECREASE_INTENSITY_SIGNAL, False)
        elif (
            not aroused
            and self.STATE.aroused
            and self.STATE.in_rem
            and self.STATE.cueing_enabled
        ):
            logger.info("Participant is no longer aroused in REM. Enabling cueing...")
            yield (self.CUEING_ENABLE_SIGNAL, True)

        self.STATE.aroused = aroused

    async def _wake_up(self) -> AsyncGenerator:
        self.STATE.experiment_state = ExperimentState.WAKING
        yield (self.CUEING_ENABLE_SIGNAL, False)

        while self.STATE.experiment_state != ExperimentState.WAKE:
            yield (self.WAKE_UP_SIGNAL, self.SETTINGS.wake_up_signal)
            logger.info("Wake up signal sent", signal=self.SETTINGS.wake_up_signal)
            await asyncio.sleep(self.SETTINGS.wake_up_signal_interval)
