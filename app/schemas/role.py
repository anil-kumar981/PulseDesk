from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PermissionBase(BaseModel):
    name: str
    resource: str
    action: str
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: UUID
    role_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: UUID
    created_at: datetime
    permissions: List[PermissionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
