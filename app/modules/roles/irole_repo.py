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

class IPermissionRepo(IBaseRepo[Permission]):
    @abstractmethod
    async def get_by_role_id(self, role_id: str) -> List[Permission]:
        pass

    @abstractmethod
    async def clear_role_permissions(self, role_id: str) -> None:
        pass
