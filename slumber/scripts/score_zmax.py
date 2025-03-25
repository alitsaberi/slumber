import argparse
from pathlib import Path

import mne
import numpy as np
from loguru import logger

from slumber import MODELS_DIR
from slumber.processing.sleep_scoring import UTimeModel, score
from slumber.processing.transforms import FIRFilter
from slumber.sources.zmax import SAMPLE_RATE
from slumber.utils.data import Data

EEG_CHANNELS: list[str] = ["EEG L", "EEG R"]
FILE_EXTENSION = "edf"
PREDICTION_FILE_NAME = "utime_predictions.csv"
FILTER_LOW_CUTOFF = 0.3
FILTER_HIGH_CUTOFF = 30
DEFAULT_MODEL = "utime_EEG_10"


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score sleep stages from ZMax data")
    parser.add_argument("data_dir", type=Path, help="Path to ZMax data directory")
    parser.add_argument(
        "--model-dir",
        type=Path,
        help="Path to directory containing U-Time model",
        default=MODELS_DIR / DEFAULT_MODEL,
    )
    parser.add_argument(
        "--weight-file",
        type=str,
        help="Name of specific weight file to use",
        default=None,
    )
    parser.add_argument(
        "--no-filter",
        action="store_true",
        help="Do not apply a filter to the data",
    )
    parser.add_argument(
        "--epoch_duration",
        type=int,
        help="Duration of epochs in seconds",
        default=30,
    )
    parser.add_argument(
        "--output-path", type=Path, help="Path to save output predictions", default=None
    )
    return parser


def _read_raw_data(data_dir: Path, data_type: str) -> mne.io.Raw:
    logger.info(f"Extracting {data_type}")
    data_type_file = data_dir / f"{data_type}.{FILE_EXTENSION}"
    raw = mne.io.read_raw_edf(data_type_file, preload=False)
    return raw.get_data().squeeze()


def _load_data(data_dir: Path) -> Data:
    array = np.column_stack(
        [_read_raw_data(data_dir, data_type) for data_type in EEG_CHANNELS]
    )
    data = Data(array, sample_rate=SAMPLE_RATE, channel_names=EEG_CHANNELS)
    logger.debug(f"Loaded data: {data}")
    return data


def _resample_predictions(predictions: Data, epoch_duration: int) -> Data:
    logger.info(f"Resampling predictions to {epoch_duration}-second epochs")
    periods_to_aggregate = int(epoch_duration * predictions.sample_rate)
    n_complete_epochs = predictions.length // periods_to_aggregate
    reshaped_array = predictions.array[
        : n_complete_epochs * periods_to_aggregate
    ].reshape(n_complete_epochs, periods_to_aggregate, -1)
    aggregated_array = np.mean(reshaped_array, axis=1)
    new_sample_rate = 1 / epoch_duration
    predictions = Data(
        array=aggregated_array,
        sample_rate=new_sample_rate,
        channel_names=predictions.channel_names,
    )
    logger.debug(f"Resampled predictions: {predictions}")
    return predictions


def main() -> None:
    args = _get_parser().parse_args()

    logger.info(f"Loading data from {args.data_dir}")
    data = _load_data(args.data_dir)

    if not args.no_filter:
        logger.info(
            f"Applying FIR filter with low cutoff {FILTER_LOW_CUTOFF}"
            f" and high cutoff {FILTER_HIGH_CUTOFF}"
        )
        data = FIRFilter()(
            data, low_cutoff=FILTER_LOW_CUTOFF, high_cutoff=FILTER_HIGH_CUTOFF
        )

    logger.info(f"Loading model from {args.model_dir}")
    model = UTimeModel(args.model_dir, weight_file_name=args.weight_file)
    model.n_periods = int(
        np.ceil(data.duration.total_seconds() / model.period_duration)
    )

    logger.info("Scoring sleep stages")
    predictions = score(
        data, model, channel_groups=[[ch] for ch in EEG_CHANNELS], arg_max=False
    )

    if predictions.sample_rate != 1 / args.epoch_duration:
        logger.info(
            f"Epoch duration {args.epoch_duration}"
            " does not match predictions sample rate."
        )
        predictions = _resample_predictions(predictions, args.epoch_duration)

    output_path = args.output_path or args.data_dir / PREDICTION_FILE_NAME
    logger.info(f"Saving predictions to {output_path}")
    predictions.to_csv(output_path)


if __name__ == "__main__":
    main()
