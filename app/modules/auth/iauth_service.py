from abc import ABC, abstractmethod
from fastapi import Request
from app.schemas.auth import (
    RegisterRequest,
    VerifyOTPRequest,
    LoginRequest,
    LoginVerifyRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.shared.api_response import ApiResponse

class IAuthService(ABC):
    @abstractmethod
    async def register_request_otp(self, request: RegisterRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def register_verify_otp(self, request: VerifyOTPRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def login_request_otp(self, request: LoginRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def login_verify_otp(self, request: LoginVerifyRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def forgot_password_request_otp(self, request: ForgotPasswordRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def forgot_password_verify_otp(self, request: VerifyOTPRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def forgot_password_reset(self, request: ResetPasswordRequest) -> ApiResponse:
        pass

    @abstractmethod
    async def logout(self, request: Request) -> ApiResponse:
        pass
