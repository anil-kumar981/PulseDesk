from typing import Any
from fastapi import status
from app.modules.roles.irole_service import IRoleService
from app.modules.roles.irole_repo import IRoleRepo, IPermissionRepo
from app.models.role import Role
from app.models.permission import Permission
from app.modules.roles.schemas import RoleCreate, RoleUpdate, RoleResponse
from app.shared.api_response import ApiResponse

class RoleService(IRoleService):
    def __init__(self, role_repo: IRoleRepo, permission_repo: IPermissionRepo):
        self.role_repo = role_repo
        self.permission_repo = permission_repo

    async def get_all_roles(self) -> ApiResponse:
        roles = await self.role_repo.get_all_with_permissions()
        # Parse into response schemas
        data = [RoleResponse.model_validate(role) for role in roles]
        return ApiResponse.success(data=data)

    async def get_role(self, role_id: Any) -> ApiResponse:
        role = await self.role_repo.get_by_id_with_permissions(role_id)
        if not role:
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        return ApiResponse.success(data=RoleResponse.model_validate(role))

    async def create_role(self, data: RoleCreate) -> ApiResponse:
        existing = await self.role_repo.get_by_name(data.name)
        if existing:
            return ApiResponse.error("Role with this name already exists", code=status.HTTP_400_BAD_REQUEST)

        role = Role(name=data.name, description=data.description)
        created_role = await self.role_repo.create(role)

        if data.permissions:
            for p in data.permissions:
                perm = Permission(
                    role_id=created_role.id,
                    name=p.name,
                    resource=p.resource,
                    action=p.action,
                    description=p.description
                )
                await self.permission_repo.create(perm)

        # Fetch again to include permissions
        full_role = await self.role_repo.get_by_id_with_permissions(created_role.id)
        return ApiResponse.success(data=RoleResponse.model_validate(full_role), message="Role created successfully")

    async def update_role(self, role_id: Any, data: RoleUpdate) -> ApiResponse:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)

        if data.name and data.name != role.name:
            existing = await self.role_repo.get_by_name(data.name)
            if existing:
                return ApiResponse.error("Role with this name already exists", code=status.HTTP_400_BAD_REQUEST)

        update_data = data.model_dump(exclude_unset=True)
        await self.role_repo.update(role_id, update_data)

        full_role = await self.role_repo.get_by_id_with_permissions(role_id)
        return ApiResponse.success(data=RoleResponse.model_validate(full_role), message="Role updated successfully")

    async def delete_role(self, role_id: Any) -> ApiResponse:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return ApiResponse.error("Role not found", code=status.HTTP_404_NOT_FOUND)
        
        await self.role_repo.delete(role_id)
        return ApiResponse.success(message="Role deleted successfully")
