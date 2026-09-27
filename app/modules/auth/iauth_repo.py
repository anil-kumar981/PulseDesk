from abc import abstractmethod
from typing import Optional
import uuid
from app.models.auth_otp import AuthOTP

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
