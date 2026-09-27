from abc import abstractmethod
from typing import Optional
import uuid
from app.models.auth_otp import AuthOTP
from app.models.reset_token import ResetToken

class IAuthRepo:
    # OTP methods
    @abstractmethod
    async def create_otp(self, otp: AuthOTP) -> AuthOTP:
        pass
        
    @abstractmethod
    async def get_latest_otp(self, email: str, purpose: str) -> Optional[AuthOTP]:
        pass
        
    @abstractmethod
    async def update_otp(self, otp: AuthOTP) -> AuthOTP:
        pass
        
    @abstractmethod
    async def delete_otp(self, id: uuid.UUID) -> None:
        pass
        
    # Reset Token methods
    @abstractmethod
    async def create_reset_token(self, reset_token: ResetToken) -> ResetToken:
        pass
        
    @abstractmethod
    async def get_reset_token_by_hash(self, token_hash: str) -> Optional[ResetToken]:
        pass
        
    @abstractmethod
    async def consume_reset_token(self, id: uuid.UUID) -> None:
        pass
