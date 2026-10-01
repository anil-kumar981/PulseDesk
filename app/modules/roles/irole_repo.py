from abc import abstractmethod
from typing import Optional, List
from app.utils.ibase_repo import IBaseRepo
from app.models.role import Role
from app.models.permission import Permission

class IRoleRepo(IBaseRepo[Role]):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_all_with_permissions(self) -> List[Role]:
        pass

    @abstractmethod
    async def get_by_id_with_permissions(self, id: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def assign_permission(self, role: Role, permission: Permission) -> None:
        pass

    @abstractmethod
    async def revoke_permission(self, role: Role, permission: Permission) -> None:
        pass
