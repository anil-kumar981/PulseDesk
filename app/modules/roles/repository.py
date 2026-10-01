from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.utils.base_repo import BaseRepo
from app.models.role import Role
from app.models.permission import Permission
from app.modules.roles.irole_repo import IRoleRepo

class RoleRepo(BaseRepo[Role], IRoleRepo):
    """
    Repository for managing Role entities and their relationships.
    """
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Role)

    async def get_by_name(self, name: str) -> Optional[Role]:
        """
        Retrieves a single role by its unique name.
        """
        result = await self.db_session.execute(select(Role).filter(Role.name == name))
        return result.scalar_one_or_none()

    async def get_all_with_permissions(self) -> List[Role]:
        """
        Retrieves all roles and eagerly loads their associated permissions.
        """
        result = await self.db_session.execute(
            select(Role).options(selectinload(Role.permissions))
        )
        return list(result.scalars().all())

    async def get_by_id_with_permissions(self, id: str) -> Optional[Role]:
        """
        Retrieves a single role by ID and eagerly loads its permissions.
        """
        result = await self.db_session.execute(
            select(Role)
            .filter(Role.id == id)
            .options(selectinload(Role.permissions))
        )
        return result.scalar_one_or_none()

    async def assign_permission(self, role: Role, permission: Permission) -> None:
        """
        Assigns a permission to a role in the association table.
        """
        if permission not in role.permissions:
            role.permissions.append(permission)
            await self.db_session.commit()

    async def revoke_permission(self, role: Role, permission: Permission) -> None:
        """
        Removes a permission from a role in the association table.
        """
        if permission in role.permissions:
            role.permissions.remove(permission)
            await self.db_session.commit()
