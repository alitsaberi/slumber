from pathlib import Path

import ezmsg.core as ez
from ezmsg.util.terminate import TerminateOnTotal, TerminateOnTotalSettings

from slumber.dag.units import data_collection, data_storage, sleep_scoring
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging


class SampleCollection(ez.Collection):
    DATA_COLLECTION = data_collection.ZMaxDataCollection()
    RAW_DATA_STORAGE = data_storage.HDF5Storage()
    SLEEP_SCORING = sleep_scoring.SleepScoring()
    SLEEP_SCORING_STORAGE = data_storage.HDF5Storage()
    TERMINATE = TerminateOnTotal()

    def __init__(self, config_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_yaml(config_path)

    def configure(self) -> None:
        self.DATA_COLLECTION.apply_settings(
            data_collection.Settings.model_validate(
                self.config["data_collection"]["settings"]
            )
        )
        self.RAW_DATA_STORAGE.apply_settings(
            data_storage.Settings.model_validate(
                self.config["raw_data_storage"]["settings"]
            )
        )
        self.SLEEP_SCORING.apply_settings(
            sleep_scoring.Settings.model_validate(
                self.config["sleep_scoring"]["settings"]
            )
        )
        self.SLEEP_SCORING_STORAGE.apply_settings(
            data_storage.Settings.model_validate(
                self.config["sleep_scoring_storage"]["settings"]
            )
        )
        self.TERMINATE.apply_settings(TerminateOnTotalSettings(total=13))

    # Use the network function to connect inputs and outputs of Units
    def network(self) -> ez.NetworkDefinition:
        return (
            (self.DATA_COLLECTION.OUTPUT_DATA, self.SLEEP_SCORING.INPUT_DATA),
            (self.DATA_COLLECTION.OUTPUT_DATA, self.RAW_DATA_STORAGE.DATA),
            (self.SLEEP_SCORING.OUTPUT_SCORES, self.SLEEP_SCORING_STORAGE.DATA),
            (self.SLEEP_SCORING.OUTPUT_SCORES, self.TERMINATE.INPUT_MESSAGE),
        )


if __name__ == "__main__":
    setup_logging()
    config_path = Path("./configs/sample_collection.yaml")
    collection = SampleCollection(config_path)
    ez.run(collection)
