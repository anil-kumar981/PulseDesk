from abc import abstractmethod
from typing import Any
from app.schemas.role import RoleCreate, RoleUpdate
from app.shared.api_response import ApiResponse

class IRoleService:
    @abstractmethod
    async def get_all_roles(self) -> ApiResponse:
        pass

    @abstractmethod
    async def get_role(self, role_id: Any) -> ApiResponse:
        pass

    @abstractmethod
    async def create_role(self, data: RoleCreate) -> ApiResponse:
        pass

    @abstractmethod
    async def update_role(self, role_id: Any, data: RoleUpdate) -> ApiResponse:
        pass

    @abstractmethod
    async def delete_role(self, role_id: Any) -> ApiResponse:
        pass

    @abstractmethod
    async def assign_permission(self, role_id: Any, permission_id: Any) -> ApiResponse:
        pass

    @abstractmethod
    async def revoke_permission(self, role_id: Any, permission_id: Any) -> ApiResponse:
        pass
