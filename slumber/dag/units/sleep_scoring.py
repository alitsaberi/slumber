from collections.abc import AsyncGenerator
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal

import ezmsg.core as ez
import numpy as np
from loguru import logger
from pydantic import Field, field_validator, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.processing.sleep_scoring import UTimeModel, score
from slumber.processing.transforms import Transform, get_transform_class
from slumber.utils.data import Data


class TransformConfig(PydanticSettings):
    channel_indices: list[int] = Field(min_length=1)
    target_channel_indices: list[int] = Field(min_length=1)
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

    @model_validator(mode="after")
    def validate_transform_kwargs(self) -> "TransformConfig":
        from inspect import signature

        sig = signature(self.transform.__call__)

        required_params = {
            name
            for name, param in sig.parameters.items()
            if param.default == param.empty and name not in ["self", "data", "kwargs"]
        }

        missing_params = required_params - set(self.kwargs.keys())
        if missing_params:
            raise ValueError(
                f"Missing required parameters for transform: {missing_params}"
            )

        return self

    def apply_transform(self, data: Data) -> Data:
        return self.transform(data[:, self.channel_indices], **self.kwargs)


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
                    f"Target channel indices {overlap} are used in multiple transforms"
                )
            self._all_indices.extend(config.target_channel_indices)

        if sorted(self._all_indices) != list(range(len(self._all_indices))):
            raise ValueError(
                "Target channel indices must be consecutive integers starting from 0"
            )

        return self

    @property
    def all_indices(self) -> list[int]:
        return self._all_indices


class State(ez.State):
    model: UTimeModel
    rolling_buffer: Data | None = None


class SleepScoring(ez.Unit):
    SETTINGS = Settings
    STATE = State

    INPUT_DATA = ez.InputStream(Data)
    OUTPUT_SCORES = ez.OutputStream(Data)

    async def initialize(self) -> None:
        self.STATE.model = UTimeModel(**asdict(self.SETTINGS.model))
        logger.info(f"Loaded model from {self.SETTINGS.model.model_dir}")
        self.STATE.rolling_buffer = None

    @ez.subscriber(INPUT_DATA)
    @ez.publisher(OUTPUT_SCORES)
    async def score_sleep(self, data: Data) -> AsyncGenerator:
        self._validate_data_duration(data)
        self._update_buffer(data)
        data = self._preprocess_data(data)
        scores = score(
            self.STATE.rolling_buffer,
            self.STATE.model,
            channel_groups=self.SETTINGS.channel_groups,
            arg_max=self.SETTINGS.arg_max,
        )

        yield (
            self.OUTPUT_SCORES,
            Data(
                scores[-self.STATE.model.n_samples_per_period :],
                self.STATE.model.input_sample_rate,
            ),
            # NOTE: this assumes that n_samples_per_prediction is 1
        )

    def _validate_data_duration(self, data: Data) -> None:
        """Validate that the input data duration matches the model's period duration."""
        if data.duration.total_seconds() != self.STATE.model.period_duration:
            raise ValueError(
                f"Data duration {data.duration.total_seconds()} (sec)"
                " does not match the expected duration"
                f" {self.STATE.model.period_duration} (sec)"
            )

    def _update_buffer(self, data: Data) -> None:
        if self.STATE.rolling_buffer is None:
            self.STATE.rolling_buffer = Data(
                np.zeros(
                    (
                        self.STATE.model.n_periods * data.length,
                        data.n_channels,
                    )
                ),
                data.sample_rate,
            )
            logger.info(
                "Initialized rolling buffer with shape"
                f" {self.STATE.rolling_buffer.shape}"
            )

        self.STATE.rolling_buffer.roll(-data.length)
        self.STATE.rolling_buffer[-data.length :] = data.array

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

            processed_data[:, config.target_channel_indices] = transformed_data.array

        return processed_data
