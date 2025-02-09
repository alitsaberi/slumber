from typing import Annotated, Any

import ezmsg.core as ez
import ezmsg.util as ezutil
from loguru import logger
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

from slumber.dag import units
from slumber.utils.helpers import create_class_by_name_resolver


class ComponentConfig(BaseModel):
    unit: Annotated[
        type[ez.Unit],
        BeforeValidator(create_class_by_name_resolver([units, ezutil], ez.Unit)),
    ]
    settings: dict[str, Any] = Field(default_factory=dict)
    # TODO: validate based on unit.SETTINGS

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    def configure(self) -> ez.Unit:
        if hasattr(self.unit.SETTINGS, "model_validate"):
            settings = self.unit.SETTINGS.model_validate(self.settings)
        else:
            logger.warning(
                f"Settings for {self.unit.__name__} are not validated. "
                "This may cause unexpected behavior."
            )
            settings = self.unit.SETTINGS(**self.settings)
        logger.info(f"Configured {self.unit.__name__} with settings: {settings}")
        return self.unit(settings)


class CollectionConfig(BaseModel):
    components: dict[str, ez.Unit] = Field(min_length=1)
    connections: tuple[tuple[ez.OutputStream, ez.InputStream], ...] = Field(
        default_factory=tuple
    )
    process_components: tuple[ez.Unit, ...] = Field(default_factory=tuple)
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

            try:
                stream = getattr(components[component_name], stream_name)
            except AttributeError as e:
                raise ValueError(
                    f"Invalid stream name: {stream_name} for component:"
                    f" {component_name}."
                ) from e

        return stream
