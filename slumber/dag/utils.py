from typing import Any

import ezmsg.core as ez
from pydantic import (
    ConfigDict,
    TypeAdapter,
)


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
