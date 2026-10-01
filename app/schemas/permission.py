from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from enum import Enum

class ScopeEnum(str, Enum):
    OWN = "own"
    ALL = "all"

class ActionEnum(str, Enum):
    MANAGE = "MANAGE"
    MANAGEALL = "MANAGEALL"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    FIND = "FIND"
    FINDALL = "FINDALL"
    DELETE = "DELETE"
    DELETEALL = "DELETEALL"

class PermissionBase(BaseModel):
    name: str
    resource: str
    action: ActionEnum
    scope: ScopeEnum = ScopeEnum.OWN
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[ActionEnum] = None
    scope: Optional[ScopeEnum] = None
    description: Optional[str] = None

class PermissionSimple(BaseModel):
    id: uuid.UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class PermissionResponse(PermissionBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
