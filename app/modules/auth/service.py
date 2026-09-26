import uuid
from datetime import datetime, timedelta, timezone
from fastapi import Request, Response, status
from app.core.config import config
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.models.refresh_session import RefreshSession
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.iauth_repo import IAuthRepo
from app.modules.user.iuser_repo import IUserRepo
from app.schemas.auth import LoginRequest, Token
from app.shared.api_response import ApiResponse

def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key=config.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
        max_age=config.REFRESH_TOKEN_EXPIRES_IN * 24 * 60 * 60,
    )

def clear_refresh_cookie(response: Response):
    response.delete_cookie(
        key=config.REFRESH_TOKEN_COOKIE_NAME,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
    )

class AuthService(IAuthService):
    def __init__(self, auth_repo: IAuthRepo, user_repo: IUserRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def login(self, request: LoginRequest, response: Response):
        user = await self.user_repo.get_by_email(request.email)
        
        if not user or not verify_password(request.password, user.password_hash):
            return ApiResponse.error(message="Incorrect email or password", code=status.HTTP_401_UNAUTHORIZED)
            
        session_id = uuid.uuid4()
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id), session_id=str(session_id))
        
        refresh_session = RefreshSession(
            id=session_id,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=config.REFRESH_TOKEN_EXPIRES_IN)
        )
        
        await self.auth_repo.create(refresh_session)
        
        set_refresh_cookie(response, refresh_token)
        
        # Return success with token data
        token_data = Token(access_token=access_token)
        return ApiResponse.success(data=token_data)

    async def refresh_token(self, request: Request, response: Response):
        token = request.cookies.get(config.REFRESH_TOKEN_COOKIE_NAME)
        if not token:
            token = request.headers.get("x-refresh-token")
            
        if not token:
            return ApiResponse.error(message="Missing refresh token", code=status.HTTP_401_UNAUTHORIZED)
            
        try:
            payload = verify_token(token)
        except ValueError as e:
            return ApiResponse.error(message=str(e), code=status.HTTP_401_UNAUTHORIZED)
            
        if payload.get("type") != "refresh":
            return ApiResponse.error(message="Invalid token type", code=status.HTTP_401_UNAUTHORIZED)
            
        user_id_str = payload.get("sub")
        session_id_str = payload.get("session_id")
        
        if not user_id_str or not session_id_str:
            return ApiResponse.error(message="Invalid token payload", code=status.HTTP_401_UNAUTHORIZED)
            
        session_id = uuid.UUID(session_id_str)
        
        session = await self.auth_repo.get_by_session_id(session_id)
        
        if not session:
            return ApiResponse.error(message="Session not found", code=status.HTTP_401_UNAUTHORIZED)
            
        if session.is_revoked:
            return ApiResponse.error(message="Session revoked", code=status.HTTP_401_UNAUTHORIZED)
            
        if session.expires_at < datetime.utcnow(): # naive because db uses naive internally in most local setups
            return ApiResponse.error(message="Session expired in DB", code=status.HTTP_401_UNAUTHORIZED)
            
        access_token = create_access_token(subject=user_id_str)
        token_data = Token(access_token=access_token)
        
        return ApiResponse.success(data=token_data)

    async def logout(self, request: Request, response: Response):
        token = request.cookies.get(config.REFRESH_TOKEN_COOKIE_NAME)
        if not token:
            token = request.headers.get("x-refresh-token")
            
        if token:
            try:
                payload = verify_token(token)
                if payload.get("type") == "refresh":
                    session_id = uuid.UUID(payload.get("session_id"))
                    session = await self.auth_repo.get_by_session_id(session_id)
                    if session and not session.is_revoked:
                        session.is_revoked = True
                        await self.auth_repo.update(session)
            except Exception:
                pass
                
        clear_refresh_cookie(response)
        return ApiResponse.success(message="Successfully logged out")
