"""Shared modules for DotMac applications.

This package provides shared utilities for the dotmac ecosystem:
- dotmac.shared.auth: Authentication and authorization
- dotmac.shared.db: Database utilities and Base model
- dotmac.shared.core: Caching, exceptions, and utilities
- dotmac.shared.events: Event bus and domain events
- dotmac.shared.geo: Geographic services (geocoding, routing)
- dotmac.shared.tenant: Multi-tenancy support
- dotmac.shared.integrations: Third-party integrations (NetBox, etc.)

Modules are imported on-demand to avoid circular imports.
Import directly from subpackages:
    from dotmac.shared.auth import get_current_user, hash_password
    from dotmac.shared.db import get_session_dependency, Base
    from dotmac.shared.core.caching import cache_get, cache_set
"""

__version__ = "1.0.0"
