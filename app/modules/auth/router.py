from fastapi import APIRouter, Depends, Response, Request
from app.schemas.auth import LoginRequest, Token
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.dependencies import get_auth_service

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=None)
async def login(
    request: LoginRequest,
    response: Response,
    service: IAuthService = Depends(get_auth_service)
):
    """
    Authenticate user, create a RefreshSession, and return access/refresh tokens.
    """
    return await service.login(request, response)

@router.post("/refresh", response_model=None)
async def refresh_token(
    request: Request,
    response: Response,
    service: IAuthService = Depends(get_auth_service)
):
    """
    Use a valid refresh token to get a new access token.
    """
    return await service.refresh_token(request, response)

@router.post("/logout", response_model=None)
async def logout(
    request: Request,
    response: Response,
    service: IAuthService = Depends(get_auth_service)
):
    """
    Revoke the refresh session and clear the cookie.
    """
    return await service.logout(request, response)
