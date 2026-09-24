from typing import TypeVar, Optional, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

T = TypeVar("T")

class ApiResponse:
    """
    Standard API Response utility helper for FastAPI controllers.
    Ensures unified JSON output contracts across success, fail, error, and exception scenarios.
    """

    @staticmethod
    def _format_data(data: Optional[T]) -> Any:
        if data is None:
            return {}
        
        encoded = jsonable_encoder(data)
        
        if isinstance(encoded, list):
            return encoded
        return encoded

    @staticmethod
    def success(
        data: Optional[T] = None, 
        message: str = "Operation completed successfully", 
        code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        content = {
            "status": "success",
            "message": message,
            "data": ApiResponse._format_data(data)
        }
        return JSONResponse(status_code=code, content=content)

    @staticmethod
    def fail(
        data: Optional[T] = None, 
        message: str = "Validation failed or request payload is invalid", 
        code: int = status.HTTP_400_BAD_REQUEST
    ) -> JSONResponse:
        content = {
            "status": "fail",
            "message": message,
            "data": ApiResponse._format_data(data)
        }
        return JSONResponse(status_code=code, content=content)

    @staticmethod
    def error(
        message: str = "Not Found", 
        code: int = status.HTTP_404_NOT_FOUND,
        data: Optional[T] = None
    ) -> JSONResponse:
        content = {
            "status": "error",
            "message": message,
            "data": ApiResponse._format_data(data)
        }
        return JSONResponse(status_code=code, content=content)

    @staticmethod
    def exception(
        exc: Exception, 
        message: str = "An unexpected exception occurred", 
        code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        debug: bool = True
    ) -> JSONResponse:
        err_data = {"exception_type": exc.__class__.__name__}
        if debug:
            err_data["detail"] = str(exc)
            
        content = {
            "status": "error",
            "message": message,
            "data": err_data
        }
        return JSONResponse(status_code=code, content=content)
