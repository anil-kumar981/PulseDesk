from abc import abstractmethod
from typing import Optional
import uuid
from app.models.auth_otp import AuthOTP
from app.models.session import Session

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
        
    # Session methods
    @abstractmethod
    async def create_session(self, session: Session) -> Session:
        pass
        
    @abstractmethod
    async def get_session(self, id: uuid.UUID) -> Optional[Session]:
        pass
        
    @abstractmethod
    async def update_session(self, session: Session) -> Session:
        pass
