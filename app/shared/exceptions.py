class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(CustomException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class ValidationException(CustomException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)

class UnauthorizedException(CustomException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, 401)
