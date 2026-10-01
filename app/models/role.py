import uuid
from sqlalchemy import Column, DateTime, String, Text, Integer
from app.models.user_role import UserRole
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", secondary=UserRole.__table__, back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
