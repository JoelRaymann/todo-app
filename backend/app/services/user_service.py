from typing import Optional
from uuid import UUID
import pymongo
import pymongo.errors

# Import Data Models
from app.models.user_model import UserModel

# Import Schemas
from app.schemas.user_schema import UserAuth, UserUpdate

# Import Core
from app.core.security import get_password, verify_password


class UserService:

    @staticmethod
    async def create_user(
        user: UserAuth
    ) -> UserModel:

        user_in = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password)
        )

        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(
        email: str,
        password: str
    ) -> Optional[UserModel]:

        user = await UserService.get_user_by_email(email=email)
        if not user:
            # Handle: User Doesn't exist
            return None
        if not verify_password(
            password=password,
            hashed_password=user.hashed_password
        ):
            # Handle: User password doesn't match
            return None
        return user

    @staticmethod
    async def get_user_by_email(
        email: str
    ) -> Optional[UserModel]:

        user = await UserModel.find_one(UserModel.email == email)
        return user

    @staticmethod
    async def get_user_by_id(
        user_id: UUID
    ) -> Optional[UserModel]:

        user = await UserModel.find_one(UserModel.user_id == user_id)
        return user

    @staticmethod
    async def update_user(
        user_id: UUID,
        data: UserUpdate
    ) -> UserModel:

        user = await UserModel.find_one(UserModel.user_id == user_id)
        if not user:
            raise pymongo.errors.OperationFailure(
                "User not found"
            )
        else:
            await user.update(
                {
                    "$set": data.dict(exclude_unset=True)
                }
            )
            return user
