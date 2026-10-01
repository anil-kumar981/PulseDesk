from abc import abstractmethod
from typing import Optional, List
from app.utils.ibase_repo import IBaseRepo
from app.models.permission import Permission

class IPermissionRepo(IBaseRepo[Permission]):
    @abstractmethod
    async def get_permissions_by_role_id(self, role_id: str) -> List[Permission]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[str]) -> List[Permission]:
        pass
