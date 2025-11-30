"""Shared dependency utilities.

Contains base dependency management tools. App-specific service getters
should be defined in platform or ISP packages.
"""

from functools import lru_cache
from importlib import import_module
from typing import Any, TypeVar

T = TypeVar("T")


class DependencyError(Exception):
    """Raised when a required dependency is not available."""

    pass


class DependencyChecker:
    """Check if optional dependencies are available."""

    _cache: dict[str, bool] = {}

    @classmethod
    def is_available(cls, module_name: str) -> bool:
        """Check if a module is importable."""
        if module_name not in cls._cache:
            try:
                import_module(module_name)
                cls._cache[module_name] = True
            except ImportError:
                cls._cache[module_name] = False
        return cls._cache[module_name]


def require_dependency(module_name: str, feature_name: str) -> Any:
    """Import a module or raise DependencyError with helpful message."""
    if not DependencyChecker.is_available(module_name):
        raise DependencyError(
            f"{feature_name} requires {module_name}. "
            f"Install it with: pip install {module_name}"
        )
    return import_module(module_name)


def safe_import(module_name: str, default: T | None = None) -> T | Any:
    """Safely import a module, returning default on failure."""
    try:
        return import_module(module_name)
    except ImportError:
        return default


def require_minio() -> Any:
    """Require minio package."""
    return require_dependency("minio", "File storage")


def require_meilisearch() -> Any:
    """Require meilisearch package."""
    return require_dependency("meilisearch", "Search")


def require_cryptography() -> Any:
    """Require cryptography package."""
    return require_dependency("cryptography", "Encryption")


__all__ = [
    "DependencyChecker",
    "DependencyError",
    "require_dependency",
    "safe_import",
    "require_minio",
    "require_meilisearch",
    "require_cryptography",
]
