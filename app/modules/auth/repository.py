import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.base_repo import BaseRepo
from app.models.refresh_session import RefreshSession
from app.modules.auth.iauth_repo import IAuthRepo

class AuthRepo(BaseRepo[RefreshSession], IAuthRepo):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, RefreshSession)

    async def get_by_session_id(self, session_id: uuid.UUID) -> Optional[RefreshSession]:
        try:
            result = await self.db_session.execute(select(RefreshSession).filter(RefreshSession.id == session_id))
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
