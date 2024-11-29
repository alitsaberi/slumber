import ezmsg.core as ez
import pytest

from slumber.dag.units import arousal_detection, sleep_scoring


@pytest.fixture
def test_collection(dummy_data_generator, sample_collection_config):
    class TestCollection(ez.Collection):
        DATA_GEN = dummy_data_generator
        SLEEP_SCORING = sleep_scoring.SleepScoring()
        AROUSAL_DETECTION = arousal_detection.ArousalDetection()

        def configure(self) -> None:
            self.SLEEP_SCORING.apply_settings(
                sleep_scoring.Settings.model_validate(
                    sample_collection_config["sleep_scoring"]["settings"]
                )
            )
            self.AROUSAL_DETECTION.apply_settings(
                arousal_detection.Settings.model_validate(
                    sample_collection_config["arousal_detection"]["settings"]
                )
            )

        def network(self) -> ez.NetworkDefinition:
            return (
                (self.DATA_GEN.OUTPUT_DATA, self.SLEEP_SCORING.INPUT_DATA),
                (self.SLEEP_SCORING.OUTPUT_SCORES, self.AROUSAL_DETECTION.INPUT_SCORES),
            )

    return TestCollection()


def test_sleep_scoring_unit(test_collection):
    ez.run(test_collection)
