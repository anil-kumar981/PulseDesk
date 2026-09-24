from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db

from app.modules.user.iuser_repo import IUserRepo
from app.modules.user.user_repo import UserRepo
from app.modules.user.iuser_service import IUserService
from app.modules.user.user_service import UserService

def get_user_repo(db: AsyncSession = Depends(get_db)) -> IUserRepo:
    return UserRepo(db)

def get_user_service(repo: IUserRepo = Depends(get_user_repo)) -> IUserService:
    return UserService(repo)
