from app.utils.ibase_service import IBaseService
from app.models.user import User
from typing import Union
from fastapi.responses import JSONResponse

class IUserService(IBaseService[User]):
    async def get_by_email(self, email: str) -> Union[User, JSONResponse]:
        pass
