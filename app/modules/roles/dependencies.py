from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.modules.roles.repository import RoleRepo
from app.modules.permissions.repository import PermissionRepo
from app.modules.roles.service import RoleService
from app.modules.roles.irole_service import IRoleService

def get_role_repo(db_session: AsyncSession = Depends(get_db)) -> RoleRepo:
    return RoleRepo(db_session)

def get_permission_repo(db_session: AsyncSession = Depends(get_db)) -> PermissionRepo:
    return PermissionRepo(db_session)

def get_role_service(
    role_repo: RoleRepo = Depends(get_role_repo),
    permission_repo: PermissionRepo = Depends(get_permission_repo)
) -> IRoleService:
    return RoleService(role_repo, permission_repo)
