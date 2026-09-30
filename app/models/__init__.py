from app.models.user_role import UserRole
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.models.assignment import TicketAssignment
from app.models.status_history import TicketStatusHistory
from app.models.audit_log import AuditLog
from app.models.auth_otp import AuthOTP
from app.models.session import Session

# This ensures all models are imported and registered with the SQLAlchemy Base metadata
__all__ = [
    "Role",
    "User",
    "Permission",
    "Ticket",
    "Comment",
    "TicketAssignment",
    "TicketStatusHistory",
    "AuditLog",
    "AuthOTP",
    "Session",
    "UserRole",
]
