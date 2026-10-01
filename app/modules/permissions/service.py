from typing import Any
from fastapi import status
from app.modules.permissions.ipermission_service import IPermissionService
from app.modules.permissions.ipermission_repo import IPermissionRepo
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.shared.api_response import ApiResponse
from app.core.logger import setup_logger

logger = setup_logger("app.modules.permissions.service")

class PermissionService(IPermissionService):
    """
    Service class responsible for business logic related to Permissions.
    """
    def __init__(self, permission_repo: IPermissionRepo):
        self.permission_repo = permission_repo

    async def get_permissions_by_role_id(self, role_id: Any) -> ApiResponse:
        """
        Retrieves all permissions associated with a specific role ID.
        """
        logger.info(f"Fetching permissions for role {role_id}")
        perms = await self.permission_repo.get_permissions_by_role_id(role_id)
        data = [PermissionResponse.model_validate(p) for p in perms]
        logger.info(f"Retrieved {len(data)} permissions for role {role_id}")
        return ApiResponse.success(data=data)

    async def get_permission(self, perm_id: Any) -> ApiResponse:
        """
        Retrieves a single permission by its ID.
        """
        logger.info(f"Fetching permission {perm_id}")
        perm = await self.permission_repo.get_by_id(perm_id)
        if not perm:
            logger.warning(f"Permission {perm_id} not found")
            return ApiResponse.error("Permission not found", code=status.HTTP_404_NOT_FOUND)
        return ApiResponse.success(data=PermissionResponse.model_validate(perm))

    async def create_permission(self, data: PermissionCreate) -> ApiResponse:
        """
        Creates a new standalone permission entity.
        """
        logger.info(f"Creating new permission: {data.name}")
        perm = Permission(
            name=data.name,
            resource=data.resource,
            action=data.action.value,
            scope=data.scope.value,
            description=data.description
        )
        created = await self.permission_repo.create(perm)
        logger.info(f"Permission {created.id} created successfully")
        return ApiResponse.success(data=PermissionResponse.model_validate(created), message="Permission created successfully")

    async def update_permission(self, perm_id: Any, data: PermissionUpdate) -> ApiResponse:
        """
        Updates an existing permission's attributes.
        """
        logger.info(f"Updating permission {perm_id}")
        perm = await self.permission_repo.get_by_id(perm_id)
        if not perm:
            logger.warning(f"Update failed: Permission {perm_id} not found")
            return ApiResponse.error("Permission not found", code=status.HTTP_404_NOT_FOUND)

        update_data = data.model_dump(exclude_unset=True)
        if "action" in update_data:
            update_data["action"] = update_data["action"].value
        if "scope" in update_data:
            update_data["scope"] = update_data["scope"].value

        await self.permission_repo.update(perm_id, update_data)
        updated = await self.permission_repo.get_by_id(perm_id)
        logger.info(f"Permission {perm_id} updated successfully")
        return ApiResponse.success(data=PermissionResponse.model_validate(updated), message="Permission updated successfully")

    async def delete_permission(self, perm_id: Any) -> ApiResponse:
        """
        Deletes a permission permanently.
        """
        logger.info(f"Attempting to delete permission {perm_id}")
        perm = await self.permission_repo.get_by_id(perm_id)
        if not perm:
            logger.warning(f"Delete failed: Permission {perm_id} not found")
            return ApiResponse.error("Permission not found", code=status.HTTP_404_NOT_FOUND)
        
        await self.permission_repo.delete(perm_id)
        logger.info(f"Permission {perm_id} deleted successfully")
        return ApiResponse.success(message="Permission deleted successfully")
