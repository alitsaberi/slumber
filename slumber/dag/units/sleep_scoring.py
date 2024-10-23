import logging
from collections.abc import AsyncGenerator
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal

import ezmsg.core as ez
import numpy as np
from pydantic import Field, field_validator, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.processing.sleep_scoring import UTimeModel, score
from slumber.processing.transforms import Transform, get_transform_class
from slumber.utils.data import Data

logger = logging.getLogger("slumber")


class TransformConfig(PydanticSettings):
    channel_indices: list[int]
    target_channel_indices: list[int]
    transform: Transform = Field(..., alias="class_name")
    kwargs: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def validate_indices(cls, values: dict[str, Any]) -> dict[str, Any]:
        if len(values["channel_indices"]) != len(values["target_channel_indices"]):
            raise ValueError(
                "channel_indices and target_channel_indices must have the same length"
            )
        return values

    @field_validator("transform", mode="before")
    @classmethod
    def resolve_transform(cls, v: Any) -> Transform:
        if isinstance(v, str):
            return get_transform_class(v)()
        return v

    def apply_transform(self, data: Data) -> Data:
        selected_data = Data(data.array[:, self.channel_indices], data.sample_rate)
        return self.transform(selected_data, **self.kwargs)


class ModelConfig(PydanticSettings):
    model_dir: Path
    weight_file_name: str | None = None
    n_periods: int | None = None
    n_samples_per_prediction: Literal[1] = 1  # to score every data point in the signal


class Settings(PydanticSettings):
    model: ModelConfig
    transform_configs: list[TransformConfig] = Field(
        default_factory=list, alias="transforms"
    )
    channel_groups: list[list[int]] | None = None
    arg_max: bool = True

    _all_indices: list[int] = Field(default_factory=list, init=False)

    @model_validator(mode="after")
    def validate_target_channel_indices(self) -> "Settings":
        for config in self.transform_configs:
            overlap = set(config.target_channel_indices) & set(self._all_indices)
            if overlap:
                raise ValueError(
                    f"Channel indices {overlap} are used in multiple transforms"
                )
            self._all_indices.extend(config.target_channel_indices)

        return self

    @property
    def all_indices(self) -> list[int]:
        return self._all_indices


class SleepScoring(ez.Unit):
    SETTINGS = Settings

    INPUT_DATA = ez.InputStream(Data)
    OUTPUT_SCORES = ez.OutputStream(Data)

    def initialize(self) -> None:
        self._model = UTimeModel(**asdict(self.SETTINGS.model))
        logger.info(f"Loaded model from {self.SETTINGS.model.model_dir}")
        self._rolling_buffer = None

    @ez.subscriber(INPUT_DATA)
    @ez.publisher(OUTPUT_SCORES)
    async def score_sleep(self, data: Data) -> AsyncGenerator:
        data = self._preprocess_data(data)
        self._update_buffer(data)
        scores = score(
            self._rolling_buffer,
            self._model,
            channel_groups=self.SETTINGS.channel_groups,
            arg_max=self.SETTINGS.arg_max,
        )

        segment_length = int(
            (data.length / data.sample_rate) * self._model.input_sample_rate
        )

        yield (
            self.OUTPUT_SCORES,
            Data(scores[-segment_length:], self._model.input_sample_rate),
            # TODO: this assumes that n_samples_per_prediction is 1
        )

    def _preprocess_data(self, data: Data) -> Data:
        processed_data = Data(
            np.zeros((data.length, len(self.SETTINGS.all_indices))), data.sample_rate
        )
        for config in self.SETTINGS.transform_configs:
            transformed_data = config.apply_transform(data)

            if transformed_data.sample_rate != processed_data.sample_rate:
                raise ValueError(
                    f"Sample rate of transformed data {transformed_data.sample_rate}"
                    " does not match the expected sample rate"
                    f" {processed_data.sample_rate}"
                )

            processed_data.array[:, config.target_channel_indices] = (
                transformed_data.array
            )

        return processed_data

    def _update_buffer(self, data: Data) -> None:
        if self._rolling_buffer is None:
            self._rolling_buffer = Data(
                np.zeros(
                    (
                        self._model.n_periods * data.length,
                        len(self.SETTINGS.all_indices),
                    )
                ),
                data.sample_rate,
            )
            # TODO: This assumes that each period is the same duration as the input data

        self._rolling_buffer.array = np.roll(self._rolling_buffer.array, -data.length)
        self._rolling_buffer.array[-data.length :] = data.array
