"""
Service-to-Service Authentication for Platform ↔ ISP communication.

This module provides JWT-based authentication for internal service calls
between Platform and ISP applications.
"""

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from authlib.jose import JoseError, jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict


class ServiceCredentials(BaseModel):
    """Service-to-service authentication credentials."""

    model_config = ConfigDict(extra="forbid")

    service_id: str  # e.g., "platform" or "isp-tenant-123"
    service_type: str  # "platform" or "isp"
    tenant_id: str | None = None  # ISP's tenant ID (None for platform)
    permissions: list[str] = []  # Service-level permissions


# Security scheme for service tokens
service_bearer = HTTPBearer(auto_error=True)


class ServiceAuthenticator:
    """Handles service-to-service authentication."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        token_expire_minutes: int = 60,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes
        self.header = {"alg": algorithm}

    def create_service_token(
        self,
        service_id: str,
        service_type: str,
        tenant_id: str | None = None,
        permissions: list[str] | None = None,
    ) -> str:
        """Create a JWT token for service-to-service communication.

        Args:
            service_id: Unique identifier for the service
            service_type: Either "platform" or "isp"
            tenant_id: ISP's tenant ID (required for ISP services)
            permissions: List of allowed operations

        Returns:
            JWT token string
        """
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.token_expire_minutes)

        claims = {
            "sub": service_id,
            "type": "service",
            "service_type": service_type,
            "tenant_id": tenant_id,
            "permissions": permissions or [],
            "iat": now,
            "exp": expire,
            "jti": secrets.token_urlsafe(16),
        }

        token = jwt.encode(self.header, claims, self.secret_key)
        return token.decode("utf-8") if isinstance(token, bytes) else token

    def verify_service_token(self, token: str) -> ServiceCredentials:
        """Verify and decode a service token.

        Args:
            token: JWT token to verify

        Returns:
            ServiceCredentials with the token claims

        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            claims = jwt.decode(token, self.secret_key)
            claims.validate()

            if claims.get("type") != "service":
                raise JoseError("Invalid token type")

            return ServiceCredentials(
                service_id=claims.get("sub", ""),
                service_type=claims.get("service_type", ""),
                tenant_id=claims.get("tenant_id"),
                permissions=claims.get("permissions", []),
            )
        except JoseError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid service token: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Global authenticator instance (configured at app startup)
_service_auth: ServiceAuthenticator | None = None


def configure_service_auth(secret_key: str, **kwargs: Any) -> ServiceAuthenticator:
    """Configure the global service authenticator.

    This should be called during application startup.
    """
    global _service_auth
    _service_auth = ServiceAuthenticator(secret_key, **kwargs)
    return _service_auth


def get_service_auth() -> ServiceAuthenticator:
    """Get the configured service authenticator."""
    if _service_auth is None:
        raise RuntimeError(
            "Service authenticator not configured. Call configure_service_auth() first."
        )
    return _service_auth


async def get_service_credentials(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(service_bearer),
) -> ServiceCredentials:
    """FastAPI dependency to get service credentials from request.

    Usage:
        @router.post("/internal/endpoint")
        async def endpoint(
            service: ServiceCredentials = Depends(get_service_credentials)
        ):
            if service.service_type != "platform":
                raise HTTPException(403, "Platform access required")
            ...
    """
    auth = get_service_auth()
    return auth.verify_service_token(credentials.credentials)


def require_platform_service(
    service: ServiceCredentials = Depends(get_service_credentials),
) -> ServiceCredentials:
    """Dependency that requires the caller to be the Platform service."""
    if service.service_type != "platform":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Platform service can access this endpoint",
        )
    return service


def require_isp_service(
    service: ServiceCredentials = Depends(get_service_credentials),
) -> ServiceCredentials:
    """Dependency that requires the caller to be an ISP service."""
    if service.service_type != "isp":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ISP services can access this endpoint",
        )
    return service
