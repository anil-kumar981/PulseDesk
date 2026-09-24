from typing import Any, TypeVar, List, Union
from app.utils.ibase_service import IBaseService
from app.utils.ibase_repo import IBaseRepo
from app.shared.api_response import ApiResponse
from fastapi.responses import JSONResponse

T = TypeVar("T")

class BaseService(IBaseService[T]):
    def __init__(self, repo: IBaseRepo[T]):
        self.repo = repo

    async def create(self, item: Any) -> Union[T, JSONResponse]:
        try:
            return await self.repo.create(item)
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to create")

    async def update(self, id: Any, item_data: Any) -> Union[T, JSONResponse]:
        try:
            result = await self.repo.update(id, item_data)
            if not result:
                return ApiResponse.error("Resource not found")
            return result
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to update")

    async def delete(self, id: Any) -> Union[bool, JSONResponse]:
        try:
            result = await self.repo.delete(id)
            if not result:
                return ApiResponse.error("Resource not found")
            return True
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to delete")

    async def get_all(self) -> Union[List[T], JSONResponse]:
        try:
            return await self.repo.get_all()
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to retrieve")

    async def get_by_id(self, id: Any) -> Union[T, JSONResponse]:
        try:
            result = await self.repo.get_by_id(id)
            if not result:
                return ApiResponse.error("Resource not found")
            return result
        except Exception as exc:
            return ApiResponse.exception(exc, "Failed to retrieve")
