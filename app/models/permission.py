import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    
    # Resource: the module or entity this permission applies to, e.g. "User", "Role", "Ticket"
    resource = Column(String, nullable=False)
    
    # Action: the operation allowed, e.g. "MANAGE", "CREATE", "UPDATE", "FIND", "DELETE"
    action = Column(String, nullable=False)
    
    # Scope: the visibility/authorization boundary, e.g. "own" (only entities related to the user) 
    # or "all" (entities matching the resource type across the system, subject to role hierarchy)
    scope = Column(String, nullable=False, default="own")
    
    description = Column(Text, nullable=True)

    # Roles this permission is assigned to
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
