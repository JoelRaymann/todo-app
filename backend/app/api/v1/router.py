from fastapi import APIRouter

# Import Route Handlers
from app.api.v1.handlers import user_handlers

# Import Authentication
from app.api.auth.jwt import auth_router

api_vi_router = APIRouter()

api_vi_router.include_router(
    router=user_handlers.user_router,
    prefix="/users",
    tags=["users"]
)
api_vi_router.include_router(
    router=auth_router,
    prefix="/auth",
    tags=["auth"]
)
