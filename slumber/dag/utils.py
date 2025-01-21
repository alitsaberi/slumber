from typing import Annotated, Any

import ezmsg.core as ez
from loguru import logger
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    TypeAdapter,
    model_validator,
)

from slumber.dag import units
from slumber.utils.helpers import create_class_by_name_resolver


def _model_validate(cls: type, obj: Any) -> Any:
    validator = TypeAdapter(cls)
    return validator.validate_python(obj)


class PydanticSettings(ez.Settings):
    __pydantic_config__ = ConfigDict(
        strict=False, arbitrary_types_allowed=True, frozen=True
    )

    @classmethod
    def model_validate(
        cls,
        obj: Any,
    ) -> "PydanticSettings":
        return _model_validate(cls, obj)


class PydanticState(ez.State):
    __pydantic_config__ = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @classmethod
    def model_validate(
        cls,
        obj: Any,
    ) -> "PydanticSettings":
        return _model_validate(cls, obj)


class ComponentConfig(BaseModel):
    unit: Annotated[
        type[ez.Unit],
        BeforeValidator(create_class_by_name_resolver(units, ez.Unit)),
    ]
    settings: dict[str, Any] = Field(default_factory=dict)
    # TODO: validate based on unit.SETTINGS

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    def configure(self) -> ez.Unit:
        logger.debug(f"Configuring {self.unit.address}")
        settings = self.unit.SETTINGS.model_validate(self.settings)
        return self.unit(settings)


class CollectionConfig(BaseModel):
    components: dict[str, ez.Unit] = Field(min_length=1)
    connections: tuple[tuple[ez.OutputStream, ez.InputStream], ...] = Field(
        min_length=1
    )
    process_components: list[ez.Unit] | None = None
    name: str | None = Field(None, serialization_alias="root_name")

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def resolve_connections(cls, values: dict[str, Any]) -> dict[str, Any]:
        connections = values.get("connections", tuple())
        components = cls._resolve_components(values.get("components", {}))

        if (process_components := values.get("process_components")) is not None:
            values["process_components"] = tuple(
                components[component_name] for component_name in process_components
            )

        values["connections"] = tuple(
            (
                cls._resolve_stream(connection[0], components),
                cls._resolve_stream(connection[1], components),
            )
            for connection in connections
        )
        values["components"] = components

        return values

    @staticmethod
    def _resolve_components(
        components: dict[str, dict[str, Any]],
    ) -> dict[str, ez.Unit]:
        return {
            name: ComponentConfig.model_validate(component_config).configure()
            for name, component_config in components.items()
        }

    @staticmethod
    def _resolve_stream(
        stream: str, components: dict[str, ez.Unit]
    ) -> ez.InputStream | ez.OutputStream:
        if isinstance(stream, str):
            try:
                component_name, stream_name = stream.split(".")
            except ValueError as e:
                raise ValueError(
                    f"Invalid stream name: {stream}."
                    f" Expected format: <unit_name>.<stream_name>"
                ) from e

            if component_name not in components:
                raise ValueError(
                    f"Invalid component name for a stream: {component_name}. "
                    f"Expected one of: {list(components.keys())}"
                )

            stream = getattr(components[component_name], stream_name)

        return stream
