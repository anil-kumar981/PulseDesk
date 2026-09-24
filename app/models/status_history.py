import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base import Base
from app.shared.enums import TicketStatus

class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id", ondelete="CASCADE"))
    old_status = Column(Enum(TicketStatus))
    new_status = Column(Enum(TicketStatus))
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship("Ticket", backref="status_history")
    user = relationship("User", foreign_keys=[changed_by])
