import inspect
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml
from pydantic import BeforeValidator


def load_yaml(config_path: Path) -> dict:
    """Load a yaml file and return the contents as a dictionary.

    Args:
        config_path (Path): Path to the yaml file.

    Returns:
        dict: The contents of the yaml file.
    """
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config


def get_class_by_name(
    module: ModuleType, class_name: str, base_class: type | None = None
) -> type:
    """
    Retrieve a class by its name in a module,
    ensuring it is a subclass of a specified base class.

    Args:
        module (ModuleType): The Python module to search within.
        class_name (str): The name of the class to retrieve.
        base_class (type, optional):
            The base class that the target class must inherit from.

    Returns:
        type: the class object.
    """

    try:
        cls = getattr(module, class_name)
    except AttributeError as e:
        raise AttributeError(
            f"No class named '{class_name}' found in module '{module.__name__}'."
        ) from e

    if not inspect.isclass(cls):
        raise TypeError(
            f"Class '{class_name}' in module '{module.__name__}' is not a class."
        )

    if base_class is not None and not issubclass(cls, base_class):
        raise TypeError(
            f"Class '{class_name}' in module '{module.__name__}'"
            f" is not a subclass of '{base_class.__name__}'."
        )

    return cls


def enum_by_name_validator(
    enum_type: type[Enum],
) -> BeforeValidator:
    """
    Creates a pydantic validator for converting string values to enum members.

    Args:
        enum_type (type[Enum]): The Enum class to validate against

    Returns:
        BeforeValidator: An instance of pydantic.BeforeValidator
            that converts strings to enum members.
    """

    def validate(v: Any) -> Any:
        return enum_type[v] if isinstance(v, str) else v

    return BeforeValidator(validate)
