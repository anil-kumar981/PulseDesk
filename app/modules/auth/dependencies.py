from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid
from app.database.session import get_db
from app.core.security import verify_token
from app.models.user import User

from app.modules.auth.iauth_repo import IAuthRepo
from app.modules.auth.repository import AuthRepo
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.service import AuthService
from app.modules.user.iuser_repo import IUserRepo
from app.modules.user.dependencies import get_user_repo

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to validate the Bearer access token and return the User.
    """
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
        
    try:
        payload = verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type. Only access tokens are allowed.",
        )
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user ID in token",
        )
        
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
        )
        
    # Load user from DB
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
        
    return user

def get_auth_repo(db: AsyncSession = Depends(get_db)) -> IAuthRepo:
    return AuthRepo(db)

def get_auth_service(
    auth_repo: IAuthRepo = Depends(get_auth_repo),
    user_repo: IUserRepo = Depends(get_user_repo)
) -> IAuthService:
    return AuthService(auth_repo, user_repo)
