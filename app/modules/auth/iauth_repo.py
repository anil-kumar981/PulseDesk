from abc import abstractmethod
from typing import Optional
from app.utils.ibase_repo import IBaseRepo
from app.models.refresh_session import RefreshSession
import uuid

class IAuthRepo(IBaseRepo[RefreshSession]):
    @abstractmethod
    async def get_by_session_id(self, session_id: uuid.UUID) -> Optional[RefreshSession]:
        pass
