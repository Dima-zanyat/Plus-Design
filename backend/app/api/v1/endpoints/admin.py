"""Авторизация администратора."""

from fastapi import APIRouter, Depends

from app.api.deps import AdminServiceDep, AdminUser, get_current_admin
from app.schemas.auth import AdminMe, LoginRequest, TokenResponse

auth_router = APIRouter(prefix="/admin", tags=["admin"])

protected_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@auth_router.post("/login", response_model=TokenResponse, summary="Получить JWT")
async def login(payload: LoginRequest, service: AdminServiceDep) -> TokenResponse:
    return await service.get_access(payload)


@protected_router.post("/logout", summary="Выйти (клиент отбрасывает токен)")
async def logout() -> dict[str, str]:
    return {"detail": "logged out"}


@protected_router.get("/me", response_model=AdminMe, summary="Текущий администратор")
async def me(admin_username: AdminUser) -> AdminMe:
    return AdminMe(username=admin_username)
