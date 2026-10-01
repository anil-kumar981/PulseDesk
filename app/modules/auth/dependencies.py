import uuid
from functools import wraps
from typing import Callable, Optional
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.session import Session
from app.shared.security import verify_token
from app.database.session import get_db
from app.models.user import User
from app.models.role import Role
from datetime import datetime, timezone
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.service import AuthService
from app.modules.auth.repository import AuthRepo
from app.modules.user.user_repo import UserRepo
from app.shared.security import has_permission


def get_auth_service(db: AsyncSession = Depends(get_db)) -> IAuthService:
    auth_repo = AuthRepo(db)
    user_repo = UserRepo(db)
    return AuthService(auth_repo, user_repo)

def require_auth(resource: str = None, action: str = None):
    """
    Combined Decorator for Authentication & Authorization.
    - Reads Bearer token from headers.
    - Validates stateless JWT.
    - Matches JWT `device_id` against `deviceId` header.
    - Fetches user from DB with eager loaded roles/permissions.
    - Checks advanced RBAC (hierarchy & scope) via has_permission if resource and action are provided.
    - Injects `current_user` into the route kwargs.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request and db from kwargs provided by FastAPI Dependency Injection
            request: Optional[Request] = kwargs.get("request")
            db: Optional[AsyncSession] = kwargs.get("db")
            
            if not request or not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="require_auth decorator requires 'request: Request' and 'db: AsyncSession = Depends(get_db)' in route parameters"
                )
                
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
                
            token = auth_header.split(" ")[1]
            try:
                payload = verify_token(token)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
                
            user_id_str = payload.get("sub")
            session_id_str = payload.get("session_id")
            
            if not user_id_str or not session_id_str:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
                
            session_id = uuid.UUID(session_id_str)
            
            session_result = await db.execute(select(Session).filter(Session.id == session_id))
            db_session = session_result.scalar_one_or_none()
            
            if not db_session or db_session.is_revoked or db_session.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or revoked. Please login again.")
                
            # Strict header match
            if (
                request.headers.get("deviceType") != db_session.device_type or
                request.headers.get("appVersion") != db_session.app_version or
                request.headers.get("deviceId") != db_session.device_id or
                request.headers.get("device") != db_session.device or
                request.headers.get("deviceVersion") != db_session.device_version
            ):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Device verification failed. Please login again.")
                
            # Load User with RBAC details
            user_result = await db.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(Role.permissions))
                .filter(User.id == uuid.UUID(user_id_str))
            )
            user = user_result.scalar_one_or_none()
            
            if not user or not user.is_active or not user.email_verified:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
                
            # Role & Permission Check
            if resource and action:
                target_user = None
                
                # If checking a User resource, try to find the target_user from the route params
                if resource == "User":
                    target_id = kwargs.get("user_id") or kwargs.get("id")
                    if target_id:
                        if isinstance(target_id, str):
                            target_id = uuid.UUID(target_id)
                        t_res = await db.execute(
                            select(User).options(selectinload(User.roles)).filter(User.id == target_id)
                        )
                        target_user = t_res.scalar_one_or_none()
                        
                if not has_permission(user, target_user, resource, action):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, 
                        detail=f"Access denied for {action} on {resource}. Scope or hierarchy restrictions applied."
                    )
            
            # Inject current_user into request state
            request.state.current_user = user
            return await func(*args, **kwargs)
        return wrapper
    return decorator
