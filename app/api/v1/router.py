"""V1 API router — include all versioned sub-routers here.

Example:
    from app.api.v1 import items
    router.include_router(items.router, prefix="/items", tags=["items"])
"""

from fastapi import APIRouter

router = APIRouter(prefix="/v1")

# -----------------------------------------------------------------------
# Register your v1 sub-routers below.
#
# Example — after creating app/api/v1/items.py with its own APIRouter:
#
#   from app.api.v1 import items
#   router.include_router(items.router, prefix="/items", tags=["items"])
#
# Protected routes can use the bearer dependency:
#
#   from app.core.security import verify_bearer_token
#   router.include_router(
#       items.router,
#       prefix="/items",
#       tags=["items"],
#       dependencies=[Depends(verify_bearer_token)],
#   )
# -----------------------------------------------------------------------
