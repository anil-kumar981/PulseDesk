from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.user.iuser_service import IUserService
from app.modules.user.dependencies import get_user_service
from app.shared.custom_route import ResponseWrapperRoute

router = APIRouter(prefix="/users", tags=["Users"], route_class=ResponseWrapperRoute)

@router.post("/")
@require_permissions("users:create")
async def create_user(
    user: UserCreate, 
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.create(user)

@router.get("/")
@require_permissions("users:findall")
async def get_users(
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.get_all()

@router.get("/{id}")
@require_permissions("users:find")
async def get_user(
    id: int, 
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.get_by_id(id)

@router.get("/email/{email}")
@require_permissions("users:find")
async def get_user_by_email(
    email: str, 
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.get_by_email(email)

@router.put("/{id}")
@require_permissions("users:update")
async def update_user(
    id: int, 
    user: UserUpdate, 
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.update(id, user)

@router.delete("/{id}")
@require_permissions("users:delete")
async def delete_user(
    id: int, 
    service: IUserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return await service.delete(id)
