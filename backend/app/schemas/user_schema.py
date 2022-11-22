from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User Email"
    )
    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="User Username"
    )
    password: str = Field(
        ...,
        min_length=5,
        max_length=24,
        description="User Password"
    )


class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
