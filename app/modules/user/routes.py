from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.schemas.user import UserCreate, UserUpdate
from app.modules.user.iuser_service import IUserService
from app.modules.user.dependencies import get_user_service
from app.shared.custom_route import ResponseWrapperRoute

router = APIRouter(prefix="/users", tags=["Users"], route_class=ResponseWrapperRoute)

@router.post("/")
async def create_user(user: UserCreate, service: IUserService = Depends(get_user_service)):
    return await service.create(user)

@router.get("/")
async def get_users(service: IUserService = Depends(get_user_service)):
    return await service.get_all()

@router.get("/{id}")
async def get_user(id: int, service: IUserService = Depends(get_user_service)):
    return await service.get_by_id(id)

@router.get("/email/{email}")
async def get_user_by_email(email: str, service: IUserService = Depends(get_user_service)):
    return await service.get_by_email(email)

@router.put("/{id}")
async def update_user(id: int, user: UserUpdate, service: IUserService = Depends(get_user_service)):
    return await service.update(id, user)

@router.delete("/{id}")
async def delete_user(id: int, service: IUserService = Depends(get_user_service)):
    return await service.delete(id)
