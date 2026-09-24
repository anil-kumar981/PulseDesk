from app.utils.base_service import BaseService
from app.models.user import User
from app.modules.user.iuser_repo import IUserRepo
from app.modules.user.iuser_service import IUserService
from app.shared.api_response import ApiResponse
from fastapi.responses import JSONResponse
from typing import Union

class UserService(BaseService[User], IUserService):
    def __init__(self, repo: IUserRepo):
        super().__init__(repo)
        self.repo = repo

    async def get_by_email(self, email: str) -> Union[User, JSONResponse]:
        try:
            result = await self.repo.get_by_email(email)
            if not result:
                return ApiResponse.error("User not found")
            return result
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to retrieve user by email")
