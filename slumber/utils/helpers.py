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
        logger.debug(
            f"Class {class_name} not found" f" in the main module {module.__name__}"
        )

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
                    logger.debug(
                        f"Class {class_name} not found"
                        f" in submodule {full_module_name}"
                    )
                    continue
            except ImportError:
                logger.debug(f"Failed to import submodule {full_module_name}")
                continue

    raise ValueError(
        f"No class named '{class_name}' found in module"
        f" '{module.__name__}' or its submodules."
    )


def create_enum_by_name_resolver(
    enum_type: type[Enum],
) -> Callable[[Any], Any]:
    def resolve(v: Any) -> Any:
        return enum_type[v] if isinstance(v, str) else v

    return resolve


def create_class_by_name_resolver(
    module: ModuleType, base_class: type[T] | None = None
) -> Callable[[Any], Any]:
    def resolve(v: Any) -> Any:
        return get_class_by_name(v, module, base_class) if isinstance(v, str) else v

    return resolve
