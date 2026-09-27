import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.iauth_repo import IAuthRepo
from app.models.auth_otp import AuthOTP
from app.models.reset_token import ResetToken

class AuthRepo(IAuthRepo):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_otp(self, otp: AuthOTP) -> AuthOTP:
        self.db_session.add(otp)
        await self.db_session.commit()
        return otp
        
    async def get_latest_otp(self, email: str, purpose: str) -> Optional[AuthOTP]:
        result = await self.db_session.execute(
            select(AuthOTP)
            .filter(AuthOTP.email == email, AuthOTP.purpose == purpose)
            .order_by(AuthOTP.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
        
    async def update_otp(self, otp: AuthOTP) -> AuthOTP:
        self.db_session.add(otp)
        await self.db_session.commit()
        return otp
        
    async def delete_otp(self, id: uuid.UUID) -> None:
        await self.db_session.execute(delete(AuthOTP).where(AuthOTP.id == id))
        await self.db_session.commit()
        
    async def create_reset_token(self, reset_token: ResetToken) -> ResetToken:
        self.db_session.add(reset_token)
        await self.db_session.commit()
        return reset_token
        
    async def get_reset_token_by_hash(self, token_hash: str) -> Optional[ResetToken]:
        result = await self.db_session.execute(
            select(ResetToken).filter(ResetToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
        
    async def consume_reset_token(self, id: uuid.UUID) -> None:
        result = await self.db_session.execute(
            select(ResetToken).filter(ResetToken.id == id)
        )
        token = result.scalar_one_or_none()
        if token:
            token.is_consumed = True
            await self.db_session.commit()
