from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.modules.permissions.repository import PermissionRepo
from app.modules.permissions.service import PermissionService
from app.modules.permissions.ipermission_service import IPermissionService

def get_permission_repo(db_session: AsyncSession = Depends(get_db)) -> PermissionRepo:
    return PermissionRepo(db_session)

def get_permission_service(
    permission_repo: PermissionRepo = Depends(get_permission_repo)
) -> IPermissionService:
    return PermissionService(permission_repo)
