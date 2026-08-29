"""Admin."""

from fastapi import APIRouter, Depends, Response

from app.api.deps import get_current_admin, AdminUser
from app.schemas.auth import LoginRequest, TokenResponse
from app.api.deps import AdminServiceDep

auth_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

protected_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(payload: LoginRequest, service: AdminServiceDep) -> TokenResponse:
    """Login."""
    return await service.get_access(payload)


@protected_router.get("/logout")
async def logout(response: Response) -> dict[str, str]:
    """Logout"""
    response.delete_cookie(key="access_token")
    return {"detail": "logged out"}


@protected_router.get("/me")
async def me(admin_username: AdminUser):
    return {"username": admin_username}
