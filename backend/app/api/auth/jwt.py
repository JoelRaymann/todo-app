from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import ValidationError
from datetime import datetime

# Import Settings
from app.core.config import settings

# Import Models
from app.models.user_model import UserModel

# Import Schemas
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.schemas.auth_schema import TokenPayload

# Import services
from app.services.user_service import UserService

# Import Dependencies
from app.api.dependencies.user_dependencies import get_current_user

# Import Security
from app.core.security import create_access_token, create_refresh_token


# Define the Router
auth_router = APIRouter()


@auth_router.post(
    "/login",
    summary="Create access and refresh tokens for users",
    response_model=TokenSchema
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:

    user = await UserService.authenticate(
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        # Handle: Error in login
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    else:
        # Handle: Create Access and Refresh Tokens
        return {
            "access_token": create_access_token(
                subject=user.user_id,
            ),
            "refresh_token": create_refresh_token(
                subject=user.user_id
            )
        }


@auth_router.post(
    '/refresh',
    summary="Refresh token",
    status_code=status.HTTP_200_OK
)
async def refresh_token(
    refresh_token: str = Body(...)
) -> dict[str, str]:
    try:
        payload = jwt.decode(
            token=refresh_token,
            key=settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expired",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    user = await UserService.get_user_by_id(
        user_id=token_data.subject
    )

    if not user:
        # Handle: User with this token doesn't exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user in DB"
        )

    return {
        "access_token": create_access_token(
            subject=user.user_id
        ),
        "refresh_token": create_refresh_token(
            subject=user.user_id
        )
    }


@auth_router.post(
    '/test-token',
    summary="Test if the access token is valid",
    response_model=UserOut
)
async def test_token(
    user: UserModel = Depends(get_current_user)
) -> UserOut:
    return user
