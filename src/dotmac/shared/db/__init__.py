"""
Database utility package exposing shared SQLAlchemy helpers.

This package provides SQLAlchemy 2.0 database configuration and utilities
including Base classes, session management, mixins, and compatibility types.
Import semantics: ``from dotmac.shared.db import Base`` etc.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator
    from typing import Any

    from sqlalchemy.engine import Engine
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from sqlalchemy.orm import DeclarativeBase, Session

    # Type hints for exported symbols - these are defined in the stub file
    # but we need minimal declarations here for proper resolution
    Base: Any
    BaseModel: Any
    TimestampMixin: Any
    TenantMixin: Any
    SoftDeleteMixin: Any
    AuditMixin: Any
    get_db: Any
    get_async_db: Any
    get_async_session: Any
    get_async_session_context: Any
    get_database_session: Any
    get_db_session: Any
    get_async_db_session: Any
    get_session: Any
    get_session_dependency: Any
    get_sync_engine: Any
    get_async_engine: Any
    get_async_database_url: Any
    SyncSessionLocal: Any
    AsyncSessionLocal: Any
    async_session_maker: Any
    DatabaseState: Any
    snapshot_database_state: Any
    restore_database_state: Any
    configure_database_for_testing: Any
    create_all_tables: Any
    create_all_tables_async: Any
    drop_all_tables: Any
    drop_all_tables_async: Any
    check_database_health: Any
    init_db: Any
    GUID: Any

# ---------------------------------------------------------------------------
# Load database implementation from _db_impl module
# ---------------------------------------------------------------------------

_IMPL_MODULE_NAME = "dotmac.shared._db_impl"
_IMPL_PATH = Path(__file__).resolve().parent.parent / "_db_impl.py"

_IMPL_SPEC = importlib.util.spec_from_file_location(
    _IMPL_MODULE_NAME,
    _IMPL_PATH,
)

if _IMPL_SPEC is None or _IMPL_SPEC.loader is None:
    msg = f"Unable to load database implementation module from {_IMPL_PATH}"
    raise ImportError(msg)

_impl_module = importlib.util.module_from_spec(_IMPL_SPEC)
sys.modules.setdefault(_IMPL_MODULE_NAME, _impl_module)
_IMPL_SPEC.loader.exec_module(_impl_module)  # type: ignore[assignment]

# Re-export implementation symbols (keeping public API identical)
for _name in dir(_impl_module):
    if _name.startswith("_"):
        continue
    globals()[_name] = getattr(_impl_module, _name)

# ---------------------------------------------------------------------------
# Additional helpers available under dotmac.shared.db.types
# ---------------------------------------------------------------------------

from .types import JSONBCompat  # noqa: E402  (import depends on module above)

_exported = list(getattr(_impl_module, "__all__", [])) or [
    name for name in dir(_impl_module) if not name.startswith("_")
]
if "JSONBCompat" not in _exported:
    _exported.append("JSONBCompat")

__all__ = _exported

# Ensure exported types module is reachable via package attribute
types = sys.modules[__name__ + ".types"]
