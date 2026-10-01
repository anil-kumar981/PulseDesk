from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from pwdlib import PasswordHash
from app.core.config import config

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def create_access_token(subject: str, extra_claims: Dict[str, Any] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_IN)
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def get_user_level(user) -> int:
    if not hasattr(user, "roles") or not user.roles:
        return 0
    return max([role.level for role in user.roles])

def has_permission(current_user, target_user, resource: str, action: str) -> bool:
    """
    Check if current_user can perform 'action' on 'target_user' for 'resource'.
    Enforces scope ('own' vs 'all') and hierarchy level.
    """
    # System administrator check (example: super admin might have level 100)
    current_level = get_user_level(current_user)
    
    # Extract relevant permissions for the resource
    has_access = False
    for role in current_user.roles:
        for perm in role.permissions:
            if perm.resource == resource and (perm.action == action or perm.action in ["MANAGE", "MANAGEALL"]):
                scope = perm.scope
                if scope == "own":
                    if target_user and target_user.id == current_user.id:
                        has_access = True
                elif scope == "all":
                    if not target_user or target_user.id == current_user.id:
                        has_access = True
                    else:
                        target_level = get_user_level(target_user)
                        if current_level > target_level:
                            has_access = True
    return has_access
