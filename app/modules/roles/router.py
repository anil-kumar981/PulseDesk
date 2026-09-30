from fastapi import APIRouter, Depends
from typing import Any
import uuid
from app.modules.roles.schemas import RoleCreate, RoleUpdate, RoleResponse
from app.modules.roles.irole_service import IRoleService
from app.modules.roles.dependencies import get_role_service

router = APIRouter(tags=["Roles"])

@router.get("/")
async def get_all_roles(service: IRoleService = Depends(get_role_service)):
    return await service.get_all_roles()

@router.get("/{role_id}")
async def get_role(role_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    return await service.get_role(role_id)

@router.post("/")
async def create_role(data: RoleCreate, service: IRoleService = Depends(get_role_service)):
    return await service.create_role(data)

@router.put("/{role_id}")
async def update_role(role_id: uuid.UUID, data: RoleUpdate, service: IRoleService = Depends(get_role_service)):
    return await service.update_role(role_id, data)

@router.delete("/{role_id}")
async def delete_role(role_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    return await service.delete_role(role_id)
