from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from app.utils.base_repo import BaseRepo
from app.models.role import Role
from app.models.permission import Permission
from app.modules.roles.irole_repo import IRoleRepo, IPermissionRepo

class RoleRepo(BaseRepo[Role], IRoleRepo):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Role)

    async def get_by_name(self, name: str) -> Optional[Role]:
        result = await self.db_session.execute(select(Role).filter(Role.name == name))
        return result.scalar_one_or_none()

    async def get_all_with_permissions(self) -> List[Role]:
        result = await self.db_session.execute(
            select(Role).options(selectinload(Role.permissions))
        )
        return list(result.scalars().all())

    async def get_by_id_with_permissions(self, id: str) -> Optional[Role]:
        result = await self.db_session.execute(
            select(Role)
            .filter(Role.id == id)
            .options(selectinload(Role.permissions))
        )
        return result.scalar_one_or_none()

class PermissionRepo(BaseRepo[Permission], IPermissionRepo):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Permission)

    async def get_by_role_id(self, role_id: str) -> List[Permission]:
        result = await self.db_session.execute(
            select(Permission).filter(Permission.role_id == role_id)
        )
        return list(result.scalars().all())

    async def clear_role_permissions(self, role_id: str) -> None:
        await self.db_session.execute(
            delete(Permission).where(Permission.role_id == role_id)
        )
        await self.db_session.commit()
