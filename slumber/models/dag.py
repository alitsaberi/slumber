import re
from functools import cached_property
from typing import Any, TypeAlias

import ezmsg.core as ez
import ezmsg.util as ezutil
from loguru import logger
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from slumber.dag import units
from slumber.utils.helpers import create_class_by_name_resolver

StreamConnection: TypeAlias = tuple[str, str]


class ComponentConfig(BaseModel):
    name: str = Field(min_length=1, upper=True)
    unit: type[ez.Unit]
    settings: dict[str, Any] | None = None

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def validate_settings(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "unit" not in data:
            return data

        unit = create_class_by_name_resolver([units, ezutil], ez.Unit)(data["unit"])

        if "settings" in data:
            settings = data["settings"]

            if not hasattr(unit, "SETTINGS"):
                raise ValueError(
                    f"Unit {unit.__name__} does not have a SETTINGS attribute."
                )

            if not isinstance(settings, dict):
                raise ValueError(
                    f"Settings must be a dictionary, not {type(settings)}."
                )

            if hasattr(unit.SETTINGS, "model_validate"):
                unit.SETTINGS.model_validate(settings)
            else:
                logger.warning(
                    f"Settings for {unit.__name__} are not validated. "
                    "This may cause unexpected behavior."
                )
                unit.SETTINGS(**data["settings"])

        data["unit"] = unit

        return data

    @field_validator("name", mode="after")
    @classmethod
    def check_uppercase_underscore(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Z]+(?:_[A-Z]+)*", value):
            raise ValueError(
                "Must be uppercase with words separated by underscores"
                " (e.g., 'HELLO_WORLD')."
            )
        return value

    def configure(self) -> ez.Unit:
        logger.info(f"Configuring {self.unit.__name__} with settings: {self.settings}")

        if hasattr(self.unit.SETTINGS, "model_validate"):
            settings = self.unit.SETTINGS.model_validate(self.settings)
        else:
            settings = self.unit.SETTINGS(**self.settings)

        return self.unit(settings)


class CollectionConfig(BaseModel):
    components: list[ComponentConfig] = Field(min_length=1)
    connections: list[StreamConnection] = Field(default_factory=list)
    process_components: list[str] = Field(default_factory=list)

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @cached_property
    def components_mapping(self) -> dict[str, ComponentConfig]:
        return {component.name: component for component in self.components}

    def has_component(self, name: str) -> bool:
        return name in self.components_mapping

    @model_validator(mode="after")
    def validate_unique_components(self) -> "CollectionConfig":
        names = [component.name for component in self.components]
        if len(names) != len(set(names)):
            raise ValueError("Component names must be unique")
        return self

    @model_validator(mode="after")
    def validate_connections(self) -> "CollectionConfig":
        for output_stream, input_stream in self.connections:
            self._validate_stream(output_stream, ez.OutputStream)
            self._validate_stream(input_stream, ez.InputStream)

        return self

    def _validate_stream(
        self, stream: str, stream_type: type[ez.InputStream] | type[ez.OutputStream]
    ) -> None:
        try:
            component_name, stream_name = stream.split(".")
        except ValueError as e:
            raise ValueError(
                f"Invalid stream name: {stream}."
                f" Expected format: <unit_name>.<stream_name>"
            ) from e

        if not self.has_component(component_name):
            available = ", ".join(self.components_mapping.keys())
            raise ValueError(
                f"Component '{component_name}' not found."
                f" Available components: {available}"
            )

        component = self.components_mapping[component_name]
        try:
            stream_obj = getattr(component.unit, stream_name)
        except AttributeError as e:
            raise ValueError(
                f"Stream '{stream_name}' not found in component '{component_name}'. "
            ) from e

        if not isinstance(stream_obj, stream_type):
            raise ValueError(
                f"Stream '{stream}' has wrong type {type(stream_obj).__name__}. "
                f"Expected {stream_type.__name__}"
            )

    @model_validator(mode="after")
    def validate_process_components(self) -> "CollectionConfig":
        for component in self.process_components:
            if component not in self.components_mapping:
                raise ValueError(
                    f"Invalid component name for a process component: {component}. "
                    f"Expected one of: {list(self.components_mapping.keys())}"
                )

        return self

    def configure(self) -> dict[str, Any]:
        components = {
            component.name: component.configure() for component in self.components
        }
        return {
            "components": components,
            "connections": self.connections,
            "process_components": [
                components[component_name] for component_name in self.process_components
            ],
        }
