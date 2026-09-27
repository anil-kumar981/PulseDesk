from fastapi import APIRouter, Depends, Request
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.dependencies import get_auth_service
from app.schemas.auth import (
    RegisterRequest, VerifyOTPRequest, LoginRequest, LoginVerifyRequest,
    ForgotPasswordRequest, ResetPasswordRequest
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(request: RegisterRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.register_request_otp(request)

@router.post("/register/verify-otp")
async def register_verify(request: VerifyOTPRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.register_verify_otp(request)

@router.post("/login/request-otp")
async def login_request(request: LoginRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.login_request_otp(request)

@router.post("/login/verify-otp")
async def login_verify(request: LoginVerifyRequest, http_request: Request, service: IAuthService = Depends(get_auth_service)):
    return await service.login_verify_otp(request, http_request)

@router.post("/forgot-password/request-otp")
async def forgot_password_request(request: ForgotPasswordRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.forgot_password_request_otp(request)

@router.post("/forgot-password/reset")
async def forgot_password_reset(request: ResetPasswordRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.forgot_password_reset(request)

@router.post("/logout")
async def logout(request: Request, service: IAuthService = Depends(get_auth_service)):
    return await service.logout(request)
