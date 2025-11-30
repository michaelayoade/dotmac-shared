"""Shared cache interfaces and protocols.

Contains base cache types and protocols. Implementations
should be in platform or ISP packages.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Protocol, TypeVar

T = TypeVar("T")


class CacheStrategy(str, Enum):
    """Cache invalidation strategy."""

    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"
    CACHE_ASIDE = "cache_aside"


class CacheNamespace(str, Enum):
    """Standard cache namespaces."""

    DEFAULT = "default"
    SESSION = "session"
    USER = "user"
    TENANT = "tenant"
    CONFIG = "config"


@dataclass
class CacheConfig:
    """Cache configuration."""

    namespace: str = "default"
    ttl_seconds: int = 300
    strategy: CacheStrategy = CacheStrategy.CACHE_ASIDE
    prefix: str = ""


@dataclass
class CacheStatistics:
    """Cache usage statistics."""

    hits: int = 0
    misses: int = 0
    size: int = 0
    evictions: int = 0


class CacheBackend(Protocol):
    """Protocol for cache backend implementations."""

    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        ...

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache."""
        ...

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        ...

    async def clear(self, pattern: str | None = None) -> None:
        """Clear cache, optionally matching pattern."""
        ...


class CacheServiceProtocol(Protocol):
    """Protocol for cache service implementations."""

    async def get(self, key: str, namespace: str | None = None) -> Any | None:
        """Get cached value."""
        ...

    async def set(
        self, key: str, value: Any, ttl: int | None = None, namespace: str | None = None
    ) -> None:
        """Set cached value."""
        ...

    async def delete(self, key: str, namespace: str | None = None) -> None:
        """Delete cached value."""
        ...

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        ...


# Decorator function signatures (implementations in platform/ISP)
def cached(
    ttl: int = 300,
    namespace: str | None = None,
    key_func: Callable[..., str] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Cache decorator placeholder - implementation in platform/ISP."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return func

    return decorator


__all__ = [
    # Types
    "CacheConfig",
    "CacheStatistics",
    "CacheNamespace",
    "CacheStrategy",
    # Protocols
    "CacheBackend",
    "CacheServiceProtocol",
    # Decorators (placeholder)
    "cached",
]
