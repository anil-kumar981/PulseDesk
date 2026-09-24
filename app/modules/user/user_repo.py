from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.base_repo import BaseRepo
from app.models.user import User
from app.modules.user.iuser_repo import IUserRepo

class UserRepo(BaseRepo[User], IUserRepo):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self.db_session.execute(select(User).filter(User.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
