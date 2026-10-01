from fastapi import APIRouter, Depends
from typing import Any
import uuid
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.modules.permissions.ipermission_service import IPermissionService
from app.modules.permissions.dependencies import get_permission_service

router = APIRouter(tags=["Permissions"])

@router.get("/role/{role_id}")
async def get_permissions_by_role_id(role_id: uuid.UUID, service: IPermissionService = Depends(get_permission_service)):
    """
    Retrieve all permissions associated with a specific role ID.
    """
    return await service.get_permissions_by_role_id(role_id)

@router.get("/{perm_id}")
async def get_permission(perm_id: uuid.UUID, service: IPermissionService = Depends(get_permission_service)):
    """
    Retrieve a single permission by its ID.
    """
    return await service.get_permission(perm_id)

@router.post("/")
async def create_permission(data: PermissionCreate, service: IPermissionService = Depends(get_permission_service)):
    """
    Create a new standalone permission in the system.
    """
    return await service.create_permission(data)

@router.put("/{perm_id}")
async def update_permission(perm_id: uuid.UUID, data: PermissionUpdate, service: IPermissionService = Depends(get_permission_service)):
    """
    Update an existing permission's attributes.
    """
    return await service.update_permission(perm_id, data)

@router.delete("/{perm_id}")
async def delete_permission(perm_id: uuid.UUID, service: IPermissionService = Depends(get_permission_service)):
    """
    Delete a permission permanently from the system.
    """
    return await service.delete_permission(perm_id)
