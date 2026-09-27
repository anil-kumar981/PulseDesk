import secrets
import string
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

# Re-use Argon2 setup specifically for OTP hashing
otp_hasher = PasswordHash((Argon2Hasher(),))

def generate_otp(length: int = 6) -> str:
    """Generate a cryptographically secure random OTP string."""
    alphabet = string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def hash_otp(otp: str) -> str:
    """Hash the OTP using Argon2."""
    return otp_hasher.hash(otp)

def verify_otp_hash(otp: str, hashed_otp: str) -> bool:
    """Verify an OTP against its Argon2 hash."""
    return otp_hasher.verify(otp, hashed_otp)

def generate_reset_token() -> str:
    """Generate a cryptographically secure token for password reset."""
    return secrets.token_urlsafe(32)

def send_email_otp(email: str, otp: str, purpose: str):
    """
    Mock email sending functionality.
    In a real app, integrate with smtplib or an email service provider.
    DO NOT log the OTP in production.
    """
    # For local development logging only. 
    print(f"[{purpose.upper()} OTP] -> {email}: {otp}")
