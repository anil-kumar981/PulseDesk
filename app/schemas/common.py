from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Pagination(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
