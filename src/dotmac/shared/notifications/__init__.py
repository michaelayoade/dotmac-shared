"""Shared notification interfaces and types.

Contains base notification types and protocols. Implementations
should be in platform or ISP packages.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol
from uuid import uuid4


class NotificationType(str, Enum):
    """Notification types."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    ALERT = "alert"


class NotificationPriority(str, Enum):
    """Notification priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class NotificationChannel(str, Enum):
    """Notification delivery channels."""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


@dataclass
class NotificationDTO:
    """Notification data transfer object."""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    message: str = ""
    type: NotificationType = NotificationType.INFO
    priority: NotificationPriority = NotificationPriority.NORMAL
    channel: NotificationChannel = NotificationChannel.IN_APP
    recipient_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    read: bool = False


class NotificationServiceProtocol(Protocol):
    """Protocol for notification service implementations."""

    async def send(
        self,
        recipient_id: str,
        title: str,
        message: str,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        **kwargs: Any,
    ) -> NotificationDTO:
        """Send a notification."""
        ...

    async def get_unread(self, recipient_id: str) -> list[NotificationDTO]:
        """Get unread notifications for recipient."""
        ...

    async def mark_read(self, notification_id: str) -> None:
        """Mark notification as read."""
        ...


__all__ = [
    # Types
    "NotificationType",
    "NotificationPriority",
    "NotificationChannel",
    "NotificationDTO",
    # Protocols
    "NotificationServiceProtocol",
]
