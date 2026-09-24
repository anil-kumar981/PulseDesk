from abc import ABC, abstractmethod
from typing import Any, List, Optional, Generic, TypeVar

T = TypeVar("T")

class IBaseRepo(ABC, Generic[T]):
    @abstractmethod
    async def create(self, item: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: Any, item_data: Any) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        pass
