from fastapi import APIRouter, Depends, Request
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.modules.auth.dependencies import require_auth
from app.modules.user.iuser_service import IUserService
from app.modules.user.dependencies import get_user_service
from app.shared.custom_route import ResponseWrapperRoute

router = APIRouter(prefix="/users", tags=["Users"], route_class=ResponseWrapperRoute)

import uuid
from typing import Dict, Any

@router.post("/")
@require_auth(resource="User", action="CREATE")
async def create_user(
    request: Request,
    user: UserCreate, 
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.create(user)

@router.get("/")
@require_auth(resource="User", action="FINDALL")
async def get_users(
    request: Request,
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_all()

@router.get("/{id}")
@require_auth(resource="User", action="FIND")
async def get_user(
    id: uuid.UUID, 
    request: Request,
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_by_id(id)

@router.get("/email/{email}")
@require_auth(resource="User", action="FIND")
async def get_user_by_email(
    email: str, 
    request: Request,
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_by_email(email)

@router.put("/{id}")
@require_auth(resource="User", action="UPDATE")
async def update_user(
    id: uuid.UUID, 
    request: Request,
    user: UserUpdate, 
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.update(id, user)

@router.delete("/{id}")
@require_auth(resource="User", action="DELETE")
async def delete_user(
    id: uuid.UUID, 
    request: Request,
    service: IUserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete(id)
