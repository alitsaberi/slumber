import argparse
import csv
from pathlib import Path

from loguru import logger

from slumber.processing.eye_movement import DEFAULTS, detect_lr_eye_movements
from slumber.sources.zmax.utils import load_data

EEG_CHANNELS: list[str] = ["EEG L", "EEG R"]
OUTPUT_FILE_NAME = "eye_movements.csv"


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score sleep stages from ZMax data")
    parser.add_argument("data_dir", type=Path, help="Path to ZMax data directory")
    parser.add_argument(
        "--output-path", type=Path, help="Path to save output predictions", default=None
    )
    parser.add_argument(
        "--difference-threshold",
        type=float,
        help="Threshold for detecting peaks in the difference signal",
        default=DEFAULTS["difference_threshold"],
    )
    parser.add_argument(
        "--amplitude-threshold",
        type=float,
        help="Threshold for filtering peaks based on opposite polarity",
        default=DEFAULTS["amplitude_threshold"],
    )
    parser.add_argument(
        "--min-same-event-gap",
        type=float,
        help="Minimum gap between neighboring peaks in the same direction",
        default=DEFAULTS["min_same_event_gap"],
    )
    parser.add_argument(
        "--max-sequence-gap",
        type=float,
        help="Maximum gap between consecutive eye movements in the same sequence",
        default=DEFAULTS["max_sequence_gap"],
    )
    parser.add_argument(
        "--low-cutoff",
        type=float,
        help="Low cutoff frequency for FIR filters",
        default=DEFAULTS["low_cutoff"],
    )
    parser.add_argument(
        "--high-cutoff",
        type=float,
        help="High cutoff frequency for FIR filters",
        default=DEFAULTS["high_cutoff"],
    )
    parser.add_argument(
        "--accepted-eye-signals",
        type=str,
        nargs="+",
        help="List of accepted eye signals. "
        "Only events with labels starting with any of these will be accepted.",
        default=[],
    )
    return parser


def main() -> None:
    args = _get_parser().parse_args()

    logger.info(f"Loading data from {args.data_dir}")
    data = load_data(args.data_dir, data_types=EEG_CHANNELS)
    data.array = data.array * 1_000_000  # Convert to microvolts

    logger.info("Detecting eye movements")
    sequences = detect_lr_eye_movements(
        data,
        left_eeg_label=EEG_CHANNELS[0],
        right_eeg_label=EEG_CHANNELS[1],
        difference_threshold=args.difference_threshold,
        amplitude_threshold=args.amplitude_threshold,
        min_same_event_gap=args.min_same_event_gap,
        max_sequence_gap=args.max_sequence_gap,
        low_cutoff=args.low_cutoff,
        high_cutoff=args.high_cutoff,
    )

    logger.info(f"Detected {len(sequences)} eye movements")

    if args.accepted_eye_signals:
        sequences = [
            event
            for event in sequences
            if any(event.label.startswith(label) for label in args.accepted_eye_signals)
        ]
        logger.info(f"Filtered {len(sequences)} eye movements")

    output_path = args.output_path or args.data_dir / OUTPUT_FILE_NAME
    with open(output_path, mode="w", newline="") as csv_file:
        fieldnames = ["start_time", "end_time", "label"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for event in sequences:
            writer.writerow(
                {
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                    "label": event.label,
                }
            )

    logger.info(f"Eye movements saved to {output_path}")


if __name__ == "__main__":
    main()
