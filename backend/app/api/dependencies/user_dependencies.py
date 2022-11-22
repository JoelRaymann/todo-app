from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

# Import App Settings
from app.core.config import settings
# Import Data Model
from app.models.user_model import UserModel
# Import Schemas
from app.schemas.auth_schema import TokenPayload
from app.services.user_service import UserService

# This will call the api automatically
# and generate the token for us
reusable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STRING}/auth/login",
    scheme_name="JWT"
)


async def get_current_user(
    token: str = Depends(reusable_oauth)
) -> UserModel:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
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

    return user
