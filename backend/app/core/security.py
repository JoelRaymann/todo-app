from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt

# Import App Settings
from app.core.config import settings

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password(
    password: str
) -> str:

    return password_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    return password_context.verify(
        secret=password,
        hash=hashed_password
    )


def create_access_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:

    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES
        )

    to_encode = {
        "exp": expires_delta,
        "subject": str(subject)
    }
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: int = None
) -> str:

    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRATION_MINUTES
        )

    to_encode = {
        "exp": expires_delta,
        "subject": str(subject)
    }
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
