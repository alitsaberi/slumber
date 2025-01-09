from collections.abc import AsyncGenerator
from typing import Annotated, Any

import ezmsg.core as ez
from pydantic import BeforeValidator, Field, model_validator

from slumber.dag.utils import PydanticSettings
from slumber.processing import transforms
from slumber.utils.data import Data
from slumber.utils.helpers import create_class_by_name_resolver


class TransformConfig(PydanticSettings):
    transform: Annotated[
        type[transforms.Transform],
        BeforeValidator(
            create_class_by_name_resolver(transforms, transforms.Transform)
        ),
    ] = Field(..., alias="class_name")
    kwargs: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_transform_kwargs(self) -> "TransformConfig":
        from inspect import signature

        sig = signature(self.transform.__call__)

        required_params = {
            name
            for name, param in sig.parameters.items()
            if param.default == param.empty and name not in ["self", "data", "kwargs"]
        }  # TODO: there might duplication with cognitive_training.py

        missing_params = required_params - set(self.kwargs.keys())
        if missing_params:
            raise ValueError(
                f"Missing required parameters for transform: {missing_params}"
            )

        return self

    def apply_transform(self, data: Data) -> Data:
        return self.transform(data, **self.kwargs)


class Settings(PydanticSettings):
    transform_configs: list[TransformConfig] = Field(
        default_factory=list, alias="transforms", min_length=1
    )


class Transform(ez.Unit):
    SETTINGS = Settings

    INPUT = ez.InputStream(Data)
    OUTPUT = ez.OutputStream(Data)

    @ez.subscriber(INPUT)
    @ez.publisher(OUTPUT)
    async def apply_transforms(
        self, data: Data
    ) -> AsyncGenerator[tuple[ez.OutputStream, Data], None]:
        for config in self.SETTINGS.transform_configs:
            data = config.apply_transform(data)

        yield (self.OUTPUT, data)
