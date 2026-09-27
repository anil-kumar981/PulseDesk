import uuid
from functools import wraps
from typing import List, Callable
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import config
from app.shared.security import verify_token
from app.database.session import get_db
from app.models.user import User
from app.models.role import Role
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.service import AuthService
from app.modules.auth.repository import AuthRepo
from app.modules.user.user_repo import UserRepo

def get_auth_service(db: AsyncSession = Depends(get_db)) -> IAuthService:
    auth_repo = AuthRepo(db)
    user_repo = UserRepo(db)
    return AuthService(auth_repo, user_repo)

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    token = request.cookies.get(config.COOKIE_NAME)
    if not token:
        # Fallback to Bearer token if not in cookie (for Swagger/Postman testing without cookies)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    try:
        payload = verify_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
    # Load user with roles and permissions eagerly
    user_result = await db.execute(
        select(User)
        .options(selectinload(User.roles).selectinload(Role.permissions))
        .filter(User.id == uuid.UUID(user_id_str))
    )
    user = user_result.scalar_one_or_none()
    
    if not user or not user.is_active or not user.email_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        
    return user

def require_permissions(*required_permissions: str):
    """
    Decorator for RBAC. Ensures the current user has all required permissions.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Ensure the route has `current_user` injected
            user: User = kwargs.get("current_user")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="require_permissions decorator requires 'current_user' dependency in the route"
                )
            
            # Collect user's permissions
            user_permissions = set()
            for role in user.roles:
                for permission in role.permissions:
                    user_permissions.add(permission.name)
            
            # Check if user has all required permissions
            for req_perm in required_permissions:
                if req_perm not in user_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, 
                        detail=f"Not enough permissions. Required: {req_perm}"
                    )
                    
            return await func(*args, **kwargs)
        return wrapper
    return decorator
