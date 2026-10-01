from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.utils.base_repo import BaseRepo
from app.models.role import Role
from app.models.permission import Permission
from app.modules.permissions.ipermission_repo import IPermissionRepo

class PermissionRepo(BaseRepo[Permission], IPermissionRepo):
    """
    Repository for managing Permission entities.
    """
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Permission)

    async def get_permissions_by_role_id(self, role_id: str) -> List[Permission]:
        """
        Retrieves all permissions associated with a specific role ID using the association table.
        """
        result = await self.db_session.execute(
            select(Permission).join(Permission.roles).filter(Role.id == role_id)
        )
        return list(result.scalars().all())

    async def get_by_ids(self, ids: List[str]) -> List[Permission]:
        """
        Retrieves a list of permissions matching the provided IDs.
        """
        result = await self.db_session.execute(
            select(Permission).filter(Permission.id.in_(ids))
        )
        return list(result.scalars().all())
