from typing import Any
from fastapi import status
from app.modules.roles.irole_service import IRoleService
from app.modules.roles.irole_repo import IRoleRepo
from app.modules.permissions.ipermission_repo import IPermissionRepo
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.shared.api_response import ApiResponse
from app.core.logger import setup_logger

logger = setup_logger("app.modules.roles.service")

class RoleService(IRoleService):
    """
    Service class responsible for business logic related to Roles and their assigned Permissions.
    """
    def __init__(self, role_repo: IRoleRepo, permission_repo: IPermissionRepo):
        self.role_repo = role_repo
        self.permission_repo = permission_repo

    async def get_all_roles(self) -> ApiResponse:
        """
        Retrieves all roles along with their eagerly loaded permissions.
        """
        logger.info("Fetching all roles with permissions")
        roles = await self.role_repo.get_all_with_permissions()
        # Parse into response schemas
        data = [RoleResponse.model_validate(role) for role in roles]
        logger.info(f"Successfully retrieved {len(data)} roles")
        return ApiResponse.success(data=data)

    async def get_role(self, role_id: Any) -> ApiResponse:
        """
        Retrieves a specific role by ID along with its permissions.
        """
        logger.info(f"Fetching role {role_id}")
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            logger.warning(f"Role {role_id} not found")
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        return ApiResponse.success(data=RoleResponse.model_validate(role))

    async def create_role(self, data: RoleCreate) -> ApiResponse:
        """
        Creates a new role and assigns the provided permissions to it.
        """
        logger.info(f"Attempting to create new role: {data.name}")
        existing = await self.role_repo.get_by_name(data.name)
        if existing:
            logger.warning(f"Role creation failed: {data.name} already exists")
            return ApiResponse.error("Role with this name already exists", code=status.HTTP_400_BAD_REQUEST)

        role = Role(name=data.name, description=data.description)
        created_role = await self.role_repo.create(role)
        logger.info(f"Created base role {created_role.id}")

        if data.permission_ids:
            logger.info(f"Assigning {len(data.permission_ids)} permissions to role {created_role.id}")
            perms = await self.permission_repo.get_by_ids(data.permission_ids)
            for p in perms:
                await self.role_repo.assign_permission(created_role, p)

        # Fetch again to include permissions
        full_role = await self.role_repo.get_by_id_with_permissions(created_role.id)
        logger.info(f"Role {full_role.id} fully constructed and returned")
        return ApiResponse.success(data=RoleResponse.model_validate(full_role), message="Role created successfully")

    async def update_role(self, role_id: Any, data: RoleUpdate) -> ApiResponse:
        """
        Updates basic role attributes (name, description). 
        Permissions are updated via dedicated assign/revoke methods.
        """
        logger.info(f"Updating role {role_id}")
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            logger.warning(f"Update failed: Role {role_id} not found")
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)

        if data.name and data.name != role.name:
            existing = await self.role_repo.get_by_name(data.name)
            if existing:
                logger.warning(f"Update failed: Name {data.name} already exists")
                return ApiResponse.error("Role with this name already exists", code=status.HTTP_400_BAD_REQUEST)

        update_data = data.model_dump(exclude_unset=True)
        await self.role_repo.update(role_id, update_data)
        
        logger.info(f"Role {role_id} successfully updated")
        full_role = await self.role_repo.get_by_id_with_permissions(role_id)
        return ApiResponse.success(data=RoleResponse.model_validate(full_role), message="Role updated successfully")

    async def delete_role(self, role_id: Any) -> ApiResponse:
        """
        Deletes a role entirely.
        """
        logger.info(f"Attempting to delete role {role_id}")
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            logger.warning(f"Delete failed: Role {role_id} not found")
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        
        await self.role_repo.delete(role_id)
        logger.info(f"Role {role_id} successfully deleted")
        return ApiResponse.success(message="Role deleted successfully")

    async def assign_permission(self, role_id: Any, permission_id: Any) -> ApiResponse:
        """
        Assigns an existing permission to a specific role.
        """
        logger.info(f"Assigning permission {permission_id} to role {role_id}")
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        
        perm = await self.permission_repo.get_by_id(permission_id)
        if not perm:
            return ApiResponse.error("Permission not found", code=status.HTTP_404_NOT_FOUND)

        await self.role_repo.assign_permission(role, perm)
        updated_role = await self.role_repo.get_by_id_with_permissions(role_id)
        logger.info(f"Permission successfully assigned")
        return ApiResponse.success(data=RoleResponse.model_validate(updated_role), message="Permission assigned successfully")

    async def revoke_permission(self, role_id: Any, permission_id: Any) -> ApiResponse:
        """
        Revokes a specific permission from a role.
        """
        logger.info(f"Revoking permission {permission_id} from role {role_id}")
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        
        perm = await self.permission_repo.get_by_id(permission_id)
        if not perm:
            return ApiResponse.error("Permission not found", code=status.HTTP_404_NOT_FOUND)

        await self.role_repo.revoke_permission(role, perm)
        updated_role = await self.role_repo.get_by_id_with_permissions(role_id)
        logger.info(f"Permission successfully revoked")
        return ApiResponse.success(data=RoleResponse.model_validate(updated_role), message="Permission revoked successfully")
