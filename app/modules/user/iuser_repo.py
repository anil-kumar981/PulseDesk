from abc import abstractmethod
from typing import Optional
from app.utils.ibase_repo import IBaseRepo
from app.models.user import User

class IUserRepo(IBaseRepo[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
