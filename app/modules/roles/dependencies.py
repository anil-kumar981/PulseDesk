from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.modules.roles.repository import RoleRepo, PermissionRepo
from app.modules.roles.service import RoleService
from app.modules.roles.irole_service import IRoleService

def get_role_service(db_session: AsyncSession = Depends(get_db)) -> IRoleService:
    role_repo = RoleRepo(db_session)
    permission_repo = PermissionRepo(db_session)
    return RoleService(role_repo, permission_repo)
