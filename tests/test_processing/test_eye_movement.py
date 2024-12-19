import numpy as np
import pytest

from slumber.processing.eye_movement import (
    MovementEvent,
    _build_sequences,
    _detect_movement_events,
    _peaks_to_events,
    detect_lr_eye_movements,
)
from slumber.utils.data import Data


@pytest.fixture
def sample_data():
    sample_rate = 100
    duration = 20
    time = np.linspace(0, 10, duration * sample_rate)
    left_channel = np.sin(2 * np.pi * 0.5 * time)
    right_channel = -np.sin(2 * np.pi * 0.5 * time)
    data = Data(
        array=np.column_stack([left_channel, right_channel]),
        sample_rate=sample_rate,
        channel_names=["left_eeg", "right_eeg"],
    )
    return data


def test_movement_event_creation():
    event = MovementEvent(label="L", start_time=1.0, end_time=2.0)
    assert event.label == "L"
    assert event.start_time == 1.0
    assert event.end_time == 2.0


def test_detect_lr_eye_movements_basic(sample_data):
    movements = detect_lr_eye_movements(
        sample_data,
        left_eeg_label="left_eeg",
        right_eeg_label="right_eeg",
        difference_threshold=0.5,
    )
    assert isinstance(movements, list)
    if movements:
        assert isinstance(movements[0], MovementEvent)


def test_detect_lr_eye_movements_empty(sample_data):
    sample_data.array = np.zeros((2000, 2))
    movements = detect_lr_eye_movements(
        sample_data, left_eeg_label="left_eeg", right_eeg_label="right_eeg"
    )
    assert movements == []


def test_peaks_to_events():
    peaks = [100, 200, 300]
    events = _peaks_to_events(peaks, 100, "L")
    assert len(events) == 3
    assert events[0].label == "L"
    assert events[0].start_time == 1.0


def test_build_sequences_single():
    events = [
        MovementEvent("L", 1.0, 1.0),
        MovementEvent("R", 1.2, 1.2),
    ]
    sequences = _build_sequences(events, max_sequence_gap=0.5)
    assert len(sequences) == 1
    assert sequences[0].label == "LR"


def test_build_sequences_multiple():
    events = [
        MovementEvent("L", 1.0, 1.0),
        MovementEvent("R", 1.2, 1.2),
        MovementEvent("L", 3.0, 3.0),
        MovementEvent("R", 3.2, 3.2),
    ]
    sequences = _build_sequences(events, max_sequence_gap=0.5)
    assert len(sequences) == 2
    assert sequences[0].label == "LR"
    assert sequences[1].label == "LR"


def test_build_sequences_empty():
    sequences = _build_sequences([], max_sequence_gap=0.5)
    assert sequences == []


def test_detect_movement_events(sample_data):
    events = _detect_movement_events(
        sample_data[:, "left_eeg"], threshold=0.5, min_same_event_gap=0.1
    )
    assert isinstance(events, list)
    if events:
        assert all(isinstance(event, MovementEvent) for event in events)
        assert all(event.label in ["L", "R"] for event in events)


def test_sequence_with_same_direction():
    events = [
        MovementEvent("L", 1.0, 1.0),
        MovementEvent("L", 1.1, 1.1),
        MovementEvent("R", 1.3, 1.3),
    ]
    sequences = _build_sequences(events, max_sequence_gap=0.5)
    assert len(sequences) == 1
    assert sequences[0].label == "LR"
