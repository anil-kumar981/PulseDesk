from abc import abstractmethod
from typing import Any
from app.schemas.permission import PermissionCreate, PermissionUpdate
from app.shared.api_response import ApiResponse

class IPermissionService:
    @abstractmethod
    async def get_permissions_by_role_id(self, role_id: Any) -> ApiResponse:
        pass

    @abstractmethod
    async def get_permission(self, perm_id: Any) -> ApiResponse:
        pass

    @abstractmethod
    async def create_permission(self, data: PermissionCreate) -> ApiResponse:
        pass

    @abstractmethod
    async def update_permission(self, perm_id: Any, data: PermissionUpdate) -> ApiResponse:
        pass

    @abstractmethod
    async def delete_permission(self, perm_id: Any) -> ApiResponse:
        pass
