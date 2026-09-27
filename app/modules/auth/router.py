from fastapi import APIRouter, Depends, Request, Response
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.dependencies import get_auth_service
from app.core.config import config
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
async def login_verify(request: LoginVerifyRequest, response: Response, service: IAuthService = Depends(get_auth_service)):
    res = await service.login_verify_otp(request)
    if res.status_code == 200 and res.data:
        access_token = res.data.access_token
        # Set JWT in HttpOnly cookie
        response.set_cookie(
            key=config.COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE,
            max_age=config.COOKIE_MAX_AGE,
        )
    return res

@router.post("/forgot-password/request-otp")
async def forgot_password_request(request: ForgotPasswordRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.forgot_password_request_otp(request)

@router.post("/forgot-password/verify-otp")
async def forgot_password_verify(request: VerifyOTPRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.forgot_password_verify_otp(request)

@router.post("/forgot-password/reset")
async def forgot_password_reset(request: ResetPasswordRequest, service: IAuthService = Depends(get_auth_service)):
    return await service.forgot_password_reset(request)

@router.post("/logout")
async def logout(response: Response, request: Request, service: IAuthService = Depends(get_auth_service)):
    res = await service.logout(request)
    response.delete_cookie(config.COOKIE_NAME)
    return res
