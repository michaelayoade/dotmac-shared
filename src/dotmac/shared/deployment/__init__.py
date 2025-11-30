"""Shared deployment interfaces.

Contains base deployment types. Full implementation is in platform.
"""

from enum import Enum
from typing import Protocol


class DeploymentState(str, Enum):
    """Deployment state."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DeploymentType(str, Enum):
    """Deployment type."""

    KUBERNETES = "kubernetes"
    DOCKER = "docker"
    VM = "vm"
    BARE_METAL = "bare_metal"


__all__ = [
    "DeploymentState",
    "DeploymentType",
]
