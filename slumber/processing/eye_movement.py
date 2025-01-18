from dataclasses import dataclass
from functools import partial
from typing import Literal

from loguru import logger
from scipy.signal import find_peaks

from slumber import settings
from slumber.processing.transforms import FIRFilter
from slumber.utils.data import Data

DEFAULTS = settings["lr_eye_movement"]

MovementType = Literal["L", "R"]


@dataclass
class MovementEvent:
    label: str
    start_time: float
    end_time: float


def detect_lr_eye_movements(
    data: Data,
    left_eeg_label: str,
    right_eeg_label: str,
    difference_threshold: float = DEFAULTS["difference_threshold"],
    min_same_event_gap: float = DEFAULTS["min_same_event_gap"],
    max_sequence_gap: float = DEFAULTS["max_sequence_gap"],
    low_cutoff: float = DEFAULTS["low_cutoff"],
    high_cutoff: float = DEFAULTS["high_cutoff"],
) -> list[MovementEvent]:
    """
    Detects left/right eye movements from EEG data.

    Args:
        data: Data object containing EEG data.
        left_eeg_label: Label for the left EEG channel.
        right_eeg_label: Label for the right EEG channel.
        difference_threshold: Threshold for detecting eye movements.
        min_same_event_gap:
            Minimum gap between neighboring peaks in the same direction.
        max_sequence_gap:
            Maximum gap between consecutive eye movements in the same sequence.
            If the gap between two eye movements is greater than this value,
            the sequence is considered complete.
        low_cutoff: Low cutoff frequency for FIR filters.
        high_cutoff: High cutoff frequency for FIR filters.

    Returns:
        List of MovementEvent objects representing detected eye movements.
        The labels are strings alternating between "L" and "R", for example "LRLR".
    """
    data = FIRFilter()(data, low_cutoff=low_cutoff, high_cutoff=high_cutoff)
    difference_data = Data(
        array=data[:, left_eeg_label].array - data[:, right_eeg_label].array,
        sample_rate=data.sample_rate,
        timestamps=data.timestamps,
    )  # TODO: Add subtraction operation to Data
    difference_data = FIRFilter()(
        difference_data, low_cutoff=low_cutoff, high_cutoff=high_cutoff
    )
    logger.debug(
        f"Difference data: {difference_data}. Max: {difference_data.array.max()}"
    )

    movement_events = _detect_movement_events(
        difference_data, difference_threshold, min_same_event_gap
    )
    sequences = _build_sequences(movement_events, max_sequence_gap)

    return sequences


def _detect_movement_events(
    data: Data, threshold: float, min_same_event_gap: float
) -> list[MovementEvent]:
    """
    Returns an ordered list of MovementEvent objects
    representing detected eye movements.
    """
    detect_peaks = partial(
        find_peaks,
        height=threshold,
        distance=min_same_event_gap * data.sample_rate,
    )
    peaks, _ = detect_peaks(data.array.squeeze())
    valleys, _ = detect_peaks(-data.array.squeeze())

    events = _peaks_to_events(peaks, data.sample_rate, "L")
    events.extend(_peaks_to_events(valleys, data.sample_rate, "R"))

    return sorted(events, key=lambda x: x.start_time)


def _peaks_to_events(
    peaks: list[int], sample_rate: int, movement_type: MovementType
) -> list[MovementEvent]:
    return [
        MovementEvent(
            label=movement_type,
            start_time=idx / sample_rate,
            end_time=idx / sample_rate,
        )
        for idx in peaks
    ]


def _build_sequences(
    events: list[MovementEvent], max_sequence_gap: float
) -> list[MovementEvent]:
    if not events:
        logger.debug("events is empty")
        return []

    sequences = []
    current_sequence = [events[0]]

    for event in events[1:]:
        if event.start_time - current_sequence[-1].end_time <= max_sequence_gap:
            if event.label == current_sequence[-1].label:
                # Extend the last event in the sequence
                current_sequence[-1].end_time = event.end_time
            else:
                current_sequence.append(event)
        else:
            sequences.append(_merge_events(current_sequence))
            current_sequence = [event]

    # Add the last sequence
    sequences.append(_merge_events(current_sequence))

    return sequences


def _merge_events(events: list[MovementEvent]) -> MovementEvent:
    return MovementEvent(
        label="".join([event.label for event in events]),
        start_time=events[0].start_time,
        end_time=events[-1].end_time,
    )
