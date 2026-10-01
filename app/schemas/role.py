from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import uuid
from datetime import datetime
from app.schemas.permission import PermissionSimple

class RoleBase(BaseModel):
    name: str
    level: int = 1
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[uuid.UUID]] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: uuid.UUID
    created_at: datetime
    permissions: List[PermissionSimple] = []

    model_config = ConfigDict(from_attributes=True)
