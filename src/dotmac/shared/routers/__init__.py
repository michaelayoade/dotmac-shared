"""Router registry utilities."""

from dotmac.shared.routers.registry import (
    RouterEntry,
    ServiceScope,
    get_all_routers,
    get_routers_for_scope,
    register_graphql_endpoint,
    register_routers_for_scope,
    validate_registry,
)

__all__ = [
    "RouterEntry",
    "ServiceScope",
    "get_all_routers",
    "get_routers_for_scope",
    "register_graphql_endpoint",
    "register_routers_for_scope",
    "validate_registry",
]
