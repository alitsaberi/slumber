import inspect
import pkgutil
from collections.abc import Callable
from enum import Enum
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, TypeVar

import yaml
from pydantic import BeforeValidator, ValidationInfo

T = TypeVar("T")


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
    module: ModuleType,
    class_name: str,
    base_class: type | None = None,
    search_submodules: bool = True,
) -> type:
    """
    Retrieve a class by its name in a module and its submodules,
    ensuring it is a subclass of a specified base class.

    Args:
        module (ModuleType): The Python module to search within.
        class_name (str): The name of the class to retrieve.
        base_class (type, optional): The base class that the target class must
            inherit from.
        search_submodules (bool): Whether to search in submodules recursively.

    Returns:
        type: the class object.
    """
    # First try in the main module
    try:
        cls = getattr(module, class_name)
        if inspect.isclass(cls) and (base_class is None or issubclass(cls, base_class)):
            return cls
    except AttributeError:
        pass

    if search_submodules:
        # Search through all submodules
        for _, name, _ in pkgutil.iter_modules(module.__path__):
            full_module_name = f"{module.__name__}.{name}"
            try:
                submodule = import_module(full_module_name)
                try:
                    cls = getattr(submodule, class_name)
                    if inspect.isclass(cls) and (
                        base_class is None or issubclass(cls, base_class)
                    ):
                        return cls
                except AttributeError:
                    continue
            except ImportError:
                continue

    raise ValueError(
        f"No class named '{class_name}' found in module"
        f" '{module.__name__}' or its submodules."
    )


def enum_by_name_validator(
    enum_type: type[Enum],
) -> BeforeValidator:
    # TODO: make this a resolver similar to resolve_class
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


def make_class_validator(
    base_class: type[T], module: ModuleType
) -> Callable[[Any, ValidationInfo], Any]:
    def validate(v: Any, info: ValidationInfo) -> Any:
        return get_class_by_name(module, v, base_class) if isinstance(v, str) else v

    return validate
