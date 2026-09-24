from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, List, Union
from fastapi.responses import JSONResponse

T = TypeVar("T")

class IBaseService(ABC, Generic[T]):
    @abstractmethod
    async def create(self, item: Any) -> Union[T, JSONResponse]:
        pass

    @abstractmethod
    async def update(self, id: Any, item_data: Any) -> Union[T, JSONResponse]:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> Union[bool, JSONResponse]:
        pass

    @abstractmethod
    async def get_all(self) -> Union[List[T], JSONResponse]:
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Union[T, JSONResponse]:
        pass
