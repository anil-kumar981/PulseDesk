from fastapi import APIRouter, Depends
from typing import Any
import uuid
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.modules.roles.irole_service import IRoleService
from app.modules.roles.dependencies import get_role_service

router = APIRouter(tags=["Roles"])

@router.get("/")
async def get_all_roles(service: IRoleService = Depends(get_role_service)):
    """
    Retrieve all roles in the system along with their associated permissions.
    """
    return await service.get_all_roles()

@router.get("/{role_id}")
async def get_role(role_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    """
    Retrieve a specific role by its ID, including its permissions.
    """
    return await service.get_role(role_id)

@router.post("/")
async def create_role(data: RoleCreate, service: IRoleService = Depends(get_role_service)):
    """
    Create a new role and optionally attach existing permissions to it via permission_ids.
    """
    return await service.create_role(data)

@router.put("/{role_id}")
async def update_role(role_id: uuid.UUID, data: RoleUpdate, service: IRoleService = Depends(get_role_service)):
    """
    Update a role's basic details (name, description). 
    """
    return await service.update_role(role_id, data)

@router.delete("/{role_id}")
async def delete_role(role_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    """
    Delete a role permanently from the system.
    """
    return await service.delete_role(role_id)

@router.post("/{role_id}/permissions/{permission_id}")
async def assign_permission(role_id: uuid.UUID, permission_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    """
    Assign a specific permission to a specific role.
    """
    return await service.assign_permission(role_id, permission_id)

@router.delete("/{role_id}/permissions/{permission_id}")
async def revoke_permission(role_id: uuid.UUID, permission_id: uuid.UUID, service: IRoleService = Depends(get_role_service)):
    """
    Revoke a specific permission from a specific role.
    """
    return await service.revoke_permission(role_id, permission_id)
