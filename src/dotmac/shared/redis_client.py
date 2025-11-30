"""
Centralized Redis Client Management.

Provides singleton Redis client with connection pooling and configuration management.
"""

import os
from collections.abc import AsyncGenerator
from typing import Any

import structlog
from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

logger = structlog.get_logger(__name__)

# Default Redis configuration from environment
_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
_REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
_REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
_REDIS_DB = int(os.getenv("REDIS_DB", "0"))

type RedisClientType = Redis[Any]
type RedisPoolType = ConnectionPool[Any]


class RedisClientManager:
    """
    Singleton Redis client manager with connection pooling.

    Features:
    - Connection pooling for performance
    - Automatic reconnection
    - Health checking
    - Graceful shutdown
    """

    _instance: "RedisClientManager | None" = None
    _pool: RedisPoolType | None = None
    _client: RedisClientType | None = None

    def __new__(cls) -> "RedisClientManager":
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(
        self,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None,
        db: int = 0,
        decode_responses: bool = True,
        max_connections: int = 50,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Redis connection pool.

        Args:
            host: Redis host (defaults to REDIS_HOST env var)
            port: Redis port (defaults to REDIS_PORT env var)
            password: Redis password (defaults to REDIS_PASSWORD env var)
            db: Redis database number
            decode_responses: Decode responses as UTF-8 strings
            max_connections: Maximum pool connections
            socket_timeout: Socket timeout in seconds
            socket_connect_timeout: Socket connect timeout in seconds
            **kwargs: Additional Redis connection parameters
        """
        if self._pool is not None:
            logger.warning("Redis client already initialized")
            return

        # Use environment defaults if not provided
        host = host or _REDIS_HOST
        port = port or _REDIS_PORT
        password = password or _REDIS_PASSWORD if _REDIS_PASSWORD else None

        try:
            # Create connection pool
            self._pool = ConnectionPool(
                host=host,
                port=port,
                password=password,
                db=db,
                decode_responses=decode_responses,
                max_connections=max_connections,
                socket_timeout=socket_timeout,
                socket_connect_timeout=socket_connect_timeout,
                **kwargs,
            )

            # Create client
            self._client = Redis(connection_pool=self._pool)

            # Test connection
            await self._client.ping()

            logger.info(
                "redis.initialized",
                host=host,
                port=port,
                db=db,
                max_connections=max_connections,
            )

        except RedisError as e:
            logger.error(
                "redis.initialization_failed",
                host=host,
                port=port,
                error=str(e),
            )
            raise

    async def close(self) -> None:
        """Close Redis connection pool."""
        if self._client:
            await self._client.close()
            self._client = None

        if self._pool:
            await self._pool.disconnect()
            self._pool = None

        logger.info("redis.closed")

    def get_client(self) -> RedisClientType:
        """
        Get Redis client instance.

        Returns:
            Redis client

        Raises:
            RuntimeError: If client not initialized
        """
        if self._client is None:
            raise RuntimeError("Redis client not initialized. Call initialize() first.")
        return self._client

    async def health_check(self) -> dict[str, Any]:
        """
        Perform Redis health check.

        Returns:
            Health status dictionary
        """
        if self._client is None:
            return {
                "status": "unhealthy",
                "message": "Redis client not initialized",
            }

        try:
            # Test ping
            await self._client.ping()

            # Get info
            info = await self._client.info()

            return {
                "status": "healthy",
                "redis_version": info.get("redis_version"),
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
                "uptime_in_seconds": info.get("uptime_in_seconds"),
            }

        except RedisError as e:
            logger.error("redis.health_check_failed", error=str(e))
            return {
                "status": "unhealthy",
                "error": str(e),
            }


# Global Redis client manager instance
redis_manager = RedisClientManager()


async def get_redis_client() -> AsyncGenerator[RedisClientType]:
    """
    FastAPI dependency for Redis client.

    Yields:
        Redis client instance

    Example:
        ```python
        @router.get("/endpoint")
        async def endpoint(redis: Redis = Depends(get_redis_client)):
            await redis.set("key", "value")
        ```
    """
    client = redis_manager.get_client()
    try:
        yield client
    except Exception as e:
        logger.error("redis.operation_failed", error=str(e))
        raise


async def init_redis() -> None:
    """
    Initialize Redis client on application startup.

    Should be called in FastAPI lifespan or startup event.

    Example:
        ```python
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await init_redis()
            yield
            await shutdown_redis()
        ```
    """
    try:
        await redis_manager.initialize()
        logger.info("redis.startup_complete")
    except Exception as e:
        logger.error("redis.startup_failed", error=str(e))
        raise RuntimeError("Redis initialization failed") from e


async def shutdown_redis() -> None:
    """
    Close Redis connections on application shutdown.

    Should be called in FastAPI lifespan or shutdown event.
    """
    try:
        await redis_manager.close()
        logger.info("redis.shutdown_complete")
    except Exception as e:
        logger.error("redis.shutdown_failed", error=str(e))


# Convenience function for direct client access
def get_redis_sync() -> RedisClientType:
    """
    Get Redis client synchronously.

    Returns:
        Redis client

    Raises:
        RuntimeError: If client not initialized

    Note:
        Use get_redis_client() dependency in FastAPI routes instead.
        This is for use in non-FastAPI contexts.
    """
    return redis_manager.get_client()
