from fastapi import APIRouter, Depends, HTTPException, Response, status
import pymongo
import pymongo.errors

# Import Data Models
from app.models.user_model import UserModel

# Import Schemas
from app.schemas.user_schema import UserAuth, UserOut, UserUpdate

# Import Services
from app.services.user_service import UserService

# Import Dependencies
from app.api.dependencies.user_dependencies import get_current_user

user_router = APIRouter()


@user_router.post(
    "/create",
    summary="Create new user",
    response_model=UserOut
)
async def create_user(
    data: UserAuth,
) -> Response:

    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )


@user_router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserOut,
    status_code=status.HTTP_200_OK
)
async def get_me(
    user: UserModel = Depends(get_current_user)
) -> UserOut:
    return user


@user_router.post(
    "/update",
    summary="Update User",
    response_model=UserOut,
    status_code=status.HTTP_200_OK
)
async def update_user(
    data: UserUpdate,
    user: UserModel = Depends(get_current_user),
) -> UserOut:

    try:
        return await UserService.update_user(
            user_id=user.user_id,
            data=data
        )
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
