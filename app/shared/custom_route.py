import json
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.shared.api_response import ApiResponse

class ResponseWrapperRoute(APIRoute):
    """
    A custom APIRoute that automatically intercepts the raw response from an endpoint,
    and wraps it inside the standard ApiResponse.success() format.
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 1. Execute the actual route
            response = await original_route_handler(request)
            
            # 2. If it's already an error or custom JSONResponse, leave it alone
            if isinstance(response, JSONResponse) and response.status_code >= 400:
                return response
                
            try:
                # 3. FastAPI has already serialized the raw data to JSON bytes, load it
                if hasattr(response, "body") and response.body:
                    data = json.loads(response.body.decode("utf-8"))
                else:
                    data = {}
                    
                # 4. Wrap it using our standard success response
                return ApiResponse.success(data=data)
            except Exception:
                return response

        return custom_route_handler
