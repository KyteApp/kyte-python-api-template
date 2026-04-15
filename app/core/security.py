"""Security dependencies for FastAPI routes."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

_bearer_scheme = HTTPBearer(auto_error=True)

BearerCredentials = Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)]


async def verify_bearer_token(
    credentials: BearerCredentials,
) -> str:
    """Validate the Authorization: Bearer <token> header.

    Returns the token string on success.
    Raises 401 if the token is missing and 403 if it does not match.
    """
    if not settings.api_bearer_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API bearer token not configured on server",
        )

    if credentials.credentials != settings.api_bearer_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid bearer token",
        )

    return credentials.credentials
