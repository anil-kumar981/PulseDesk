from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.core.config import config

# We will implement these middleware functions shortly!
# from app.middleware.exception import register_exception_handlers
# from app.middleware.logging import APILoggingMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.user.routes import router as user_router
from app.modules.tickets.router import router as ticket_router
from app.modules.roles.router import router as role_router

# Instantiate global security scheme for Swagger UI "Authorize" button
security_scheme = HTTPBearer(auto_error=False)

# Instantiate modern, asynchronous FastAPI application context
app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    dependencies=[Depends(security_scheme)],
)

# Register request logging middleware
# app.add_middleware(APILoggingMiddleware)

# Apply CORS (Cross-Origin Resource Sharing) middleware for smooth frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register centralized global exception handlers to capture system, client, and validation errors
# register_exception_handlers(app)

# Mount modular routing layers under clean namespaces
app.include_router(user_router, prefix="/api/users")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(ticket_router, prefix="/api/tickets")
app.include_router(role_router, prefix="/api/roles")

@app.get("/", tags=["Health"])
async def root_health_check():
    """
    Service health check endpoint.
    """
    return {
        "status": "healthy",
        "service": config.APP_TITLE,
        "environment": config.ENV,
        "version": config.APP_VERSION,
    }
