from abc import ABC, abstractmethod
from fastapi import Request, Response
from app.schemas.auth import LoginRequest, Token
from app.shared.api_response import ApiResponse

class IAuthService(ABC):
    @abstractmethod
    async def login(self, request: LoginRequest, response: Response):
        pass

    @abstractmethod
    async def refresh_token(self, request: Request, response: Response):
        pass

    @abstractmethod
    async def logout(self, request: Request, response: Response):
        pass
