import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import Request, status
from sqlalchemy import select, delete
from app.models.session import Session

from app.core.config import config
from app.shared.security import get_password_hash, verify_password, create_access_token, verify_token
from app.shared.otp import generate_otp, hash_otp, verify_otp_hash, send_email_otp
from app.models.auth_otp import AuthOTP
from app.models.user import User
from app.modules.auth.iauth_service import IAuthService
from app.modules.auth.iauth_repo import IAuthRepo
from app.modules.user.iuser_repo import IUserRepo
from app.schemas.auth import (
    RegisterRequest, VerifyOTPRequest, LoginRequest, LoginVerifyRequest,
    ForgotPasswordRequest, ResetPasswordRequest, Token
)
from app.shared.api_response import ApiResponse

class AuthService(IAuthService):
    def __init__(self, auth_repo: IAuthRepo, user_repo: IUserRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def _handle_otp_generation(self, email: str, purpose: str, user_id: uuid.UUID = None):
        otp = generate_otp(config.OTP_LENGTH)
        otp_hash = hash_otp(otp)
        
        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=config.OTP_EXPIRES_IN)
        
        auth_otp = AuthOTP(
            user_id=user_id,
            email=email,
            purpose=purpose,
            otp_hash=otp_hash,
            expires_at=expires_at
        )
        await self.auth_repo.create_otp(auth_otp)
        send_email_otp(email, otp, purpose)

    async def _verify_otp_logic(self, email: str, purpose: str, incoming_otp: str) -> AuthOTP:
        db_otp = await self.auth_repo.get_latest_otp(email, purpose)
        if not db_otp:
            raise ValueError("OTP not requested or expired")
            
        if db_otp.attempts >= config.MAX_OTP_ATTEMPTS:
            await self.auth_repo.delete_otp(db_otp.id)
            raise ValueError("Maximum OTP attempts reached. Please request a new OTP.")
            
        if db_otp.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            await self.auth_repo.delete_otp(db_otp.id)
            raise ValueError("OTP has expired")
            
        if not verify_otp_hash(incoming_otp, db_otp.otp_hash):
            db_otp.attempts += 1
            await self.auth_repo.update_otp(db_otp)
            raise ValueError("Invalid OTP")
            
        return db_otp

    async def _cleanup_unverified_users(self):
        one_hour_ago = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=1)
        await self.user_repo.db_session.execute(
            delete(User).where(User.email_verified == False).where(User.created_at < one_hour_ago)
        )
        await self.user_repo.db_session.commit()

    # ---------------------------------------------------------
    # REGISTRATION
    # ---------------------------------------------------------
    async def register_request_otp(self, request: RegisterRequest) -> ApiResponse:
        await self._cleanup_unverified_users()
        
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            if existing_user.email_verified:
                return ApiResponse.error("Email already registered", code=status.HTTP_400_BAD_REQUEST)
            else:
                existing_user.first_name = request.first_name
                existing_user.last_name = request.last_name
                existing_user.password_hash = get_password_hash(request.password)
                existing_user.created_at = datetime.now(timezone.utc).replace(tzinfo=None)
                await self.user_repo.update(existing_user)
        else:
            user = User(
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
                password_hash=get_password_hash(request.password),
                email_verified=False
            )
            await self.user_repo.create(user)
        
        await self._handle_otp_generation(request.email, "registration")
        return ApiResponse.success(message="OTP sent to email. Please verify to complete registration.")

    async def register_verify_otp(self, request: VerifyOTPRequest) -> ApiResponse:
        try:
            db_otp = await self._verify_otp_logic(request.email, "registration", request.otp)
        except ValueError as e:
            return ApiResponse.error(str(e), code=status.HTTP_400_BAD_REQUEST)
            
        user = await self.user_repo.get_by_email(request.email)
        if not user or user.email_verified:
            return ApiResponse.error("Registration session expired or already verified.", code=status.HTTP_400_BAD_REQUEST)
            
        user.email_verified = True
        await self.user_repo.update(user)
        await self.auth_repo.delete_otp(db_otp.id)
        
        return ApiResponse.success(message="Registration complete. You may now log in.")

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------
    async def login_request_otp(self, request: LoginRequest) -> ApiResponse:
        user = await self.user_repo.get_by_email(request.email)
        
        if not user or not user.email_verified or not verify_password(request.password, user.password_hash):
            return ApiResponse.error("Incorrect email or password", code=status.HTTP_401_UNAUTHORIZED)
            
        await self._handle_otp_generation(request.email, "login", user.id)
        return ApiResponse.success(message="OTP sent to email.")

    async def login_verify_otp(self, request: LoginVerifyRequest, http_request: Request) -> ApiResponse:
        try:
            db_otp = await self._verify_otp_logic(request.email, "login", request.otp)
        except ValueError as e:
            return ApiResponse.error(str(e), code=status.HTTP_400_BAD_REQUEST)
            
        user = await self.user_repo.get_by_email(request.email)
        if not user or not user.email_verified:
            return ApiResponse.error("User not found or unverified", code=status.HTTP_401_UNAUTHORIZED)
            
        await self.auth_repo.delete_otp(db_otp.id)
        
        device_id = http_request.headers.get("deviceId")
        if not device_id:
            return ApiResponse.error("Missing deviceId header", code=status.HTTP_400_BAD_REQUEST)
        
        session_id = uuid.uuid4()
        session = Session(
            id=session_id,
            user_id=user.id,
            device_type=device_id, # Or use http_request.headers if we want them separately
            app_version=http_request.headers.get("appVersion", ""),
            device_id=device_id,
            device=http_request.headers.get("device", ""),
            device_version=http_request.headers.get("deviceVersion", ""),
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=config.ACCESS_TOKEN_EXPIRES_IN // 1440) # rough estimate, or config
        )
        await self.auth_repo.create_session(session)
        
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={
                "device_id": device_id,
                "session_id": str(session_id)
            }
        )
        return ApiResponse.success(data=Token(access_token=access_token))

    # ---------------------------------------------------------
    # FORGOT PASSWORD
    # ---------------------------------------------------------
    async def forgot_password_request_otp(self, request: ForgotPasswordRequest) -> ApiResponse:
        user = await self.user_repo.get_by_email(request.email)
        if user and user.email_verified:
            await self._handle_otp_generation(request.email, "forgot_password", user.id)
        return ApiResponse.success(message="If the email exists, an OTP has been sent.")

    async def forgot_password_reset(self, request: ResetPasswordRequest) -> ApiResponse:
        try:
            db_otp = await self._verify_otp_logic(request.email, "forgot_password", request.otp)
        except ValueError as e:
            return ApiResponse.error(str(e), code=status.HTTP_400_BAD_REQUEST)
            
        user = await self.user_repo.get_by_email(request.email)
        if not user:
            return ApiResponse.error("User not found", code=status.HTTP_404_NOT_FOUND)
            
        user.password_hash = get_password_hash(request.new_password)
        await self.user_repo.update(user)
        
        await self.auth_repo.delete_otp(db_otp.id)
        
        return ApiResponse.success(message="Password reset successfully. You may now log in.")

    # ---------------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------------
    async def logout(self, request: Request) -> ApiResponse:
        user = getattr(request.state, "current_user", None)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = verify_token(token)
                session_id_str = payload.get("session_id")
                if session_id_str:
                    session = await self.auth_repo.get_session(uuid.UUID(session_id_str))
                    if session:
                        session.is_revoked = True
                        await self.auth_repo.update_session(session)
            except Exception:
                pass
                
        return ApiResponse.success(message="Successfully logged out")
