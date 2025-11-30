"""
Celery application factory for DotMac applications.

This module provides a factory for creating properly configured Celery instances.
Each application (Platform, ISP) should call create_celery_app() with their
specific configuration.
"""

import os
from typing import Any

from celery import Celery
from kombu import Queue

# Global celery app instance (configured by the consuming application)
celery_app: Celery | None = None


def create_celery_app(
    name: str = "dotmac",
    broker_url: str | None = None,
    result_backend: str | None = None,
    include: list[str] | None = None,
    task_routes: dict[str, Any] | None = None,
    additional_config: dict[str, Any] | None = None,
) -> Celery:
    """Create and configure a Celery application.

    Args:
        name: Application name for Celery
        broker_url: Celery broker URL (default: from CELERY_BROKER_URL env)
        result_backend: Celery result backend URL (default: from CELERY_RESULT_BACKEND env)
        include: List of task modules to auto-discover
        task_routes: Custom task routing configuration
        additional_config: Additional Celery configuration options

    Returns:
        Configured Celery application instance
    """
    global celery_app

    # Get URLs from environment if not provided
    _broker_url = broker_url or os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    _result_backend = result_backend or os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    app = Celery(
        name,
        broker=_broker_url,
        backend=_result_backend,
        include=include or [],
    )

    # Default configuration
    default_config = {
        # Queue configuration
        "task_default_queue": "default",
        "task_queues": (
            Queue("default", routing_key="default"),
            Queue("high_priority", routing_key="high_priority"),
            Queue("low_priority", routing_key="low_priority"),
        ),
        # Task execution settings
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "timezone": "UTC",
        "enable_utc": True,
        # Task result settings
        "result_expires": 3600,  # 1 hour
        "task_track_started": True,
        "task_time_limit": 300,  # 5 minutes
        "task_soft_time_limit": 240,  # 4 minutes
        # Worker settings
        "worker_prefetch_multiplier": 1,
        "task_acks_late": True,
        "worker_max_tasks_per_child": 1000,
        # Monitoring
        "worker_send_task_events": True,
        "task_send_sent_event": True,
    }

    # Apply task routes if provided
    if task_routes:
        default_config["task_routes"] = task_routes

    # Merge with additional config
    if additional_config:
        default_config.update(additional_config)

    app.conf.update(**default_config)

    # Store as global for imports like `from dotmac.shared.celery_app import celery_app`
    celery_app = app

    return app


def get_celery_app() -> Celery:
    """Get the current Celery application.

    Raises:
        RuntimeError: If Celery app hasn't been created yet
    """
    if celery_app is None:
        raise RuntimeError(
            "Celery app not configured. Call create_celery_app() first."
        )
    return celery_app


# Create a default lazy instance that uses environment variables
# This allows `from dotmac.shared.celery_app import celery_app` to work
# but configuration should still be done explicitly by the consuming app
class _LazyCeleryApp:
    """Lazy Celery app that initializes on first access."""

    _app: Celery | None = None

    def __getattr__(self, name: str) -> Any:
        if self._app is None:
            self._app = create_celery_app()
        return getattr(self._app, name)


# Default lazy instance
celery_app = _LazyCeleryApp()  # type: ignore[assignment]


__all__ = [
    "create_celery_app",
    "get_celery_app",
    "celery_app",
]
