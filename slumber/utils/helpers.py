import inspect
import pkgutil
from collections.abc import Callable
from enum import Enum
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any, TypeVar

import yaml
from loguru import logger

T = TypeVar("T", bound=type)


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
    class_name: str,
    module: ModuleType,
    base_class: type[T] | None = None,
    search_submodules: bool = True,
) -> type[T]:
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

    def find_class_in_module(mod: ModuleType) -> type[T] | None:
        """Helper function to find the class within a module."""
        try:
            cls = getattr(mod, class_name)
            if inspect.isclass(cls) and (
                base_class is None or issubclass(cls, base_class)
            ):
                return cls
        except AttributeError:
            pass  # Class not found in this module
        return None

    # Check in the main module
    if cls := find_class_in_module(module):
        return cls

    if search_submodules and hasattr(module, "__path__"):
        # Recursively search submodules
        for _, name, _ in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
            try:
                submodule = import_module(name)
                if cls := find_class_in_module(submodule):
                    return cls
            except ImportError as e:
                logger.debug(f"Failed to import submodule {name}: {e}")

    raise ValueError(
        f"No class named '{class_name}' found in module"
        f"'{module.__name__}' or its submodules."
    )


def create_enum_by_name_resolver(
    enum_type: type[Enum],
) -> Callable[[Any], Any]:
    def resolve(v: Any) -> Any:
        return enum_type[v] if isinstance(v, str) else v

    return resolve


def create_class_by_name_resolver(
    modules: ModuleType | list[ModuleType], base_class: type[T] | None = None
) -> Callable[[Any], Any]:
    if not isinstance(modules, list):
        modules = [modules]

    def resolve(v: Any) -> Any:
        for module in modules:
            try:
                cls = (
                    get_class_by_name(v, module, base_class)
                    if isinstance(v, str)
                    else v
                )
                return cls
            except ValueError as e:
                logger.debug(e)
                continue

        raise ValueError(f"No class named '{v}' found in modules {modules}")

    return resolve
