from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Optional


class UserModel(Document):

    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False

    def __repr__(
        self
    ) -> str:
        """
        An in-built function to generate
        a debug representational string
        for the User Model.

        Returns:
            str: The debuggable representational
            string for the user model object.
        """
        return f"<User Model: {self.email}>"

    def __str__(
        self
    ) -> str:
        """
        An in-built function to print the User Model
        in human-readable format.

        Returns:
            str: A human-readable version of the User Model.
        """
        return f"""
        User Name: {self.first_name.capitalize()} {self.last_name.capitalize()}
        Email: {self.email}
        """

    def __hash__(
        self
    ) -> int:
        return hash(self.email)

    def __eq__(
        self,
        other: object
    ) -> bool:
        """
        An in-built Function to check for equality between two
        User model objects by checking their email ID.

        Args:
            other (object): An object to check equality against.

        Returns:
            bool: Returns True if both User Models are same.
        """
        if isinstance(other, UserModel):
            return self.email == other.email
        else:
            return False

    @property
    def created_on(
        self
    ) -> datetime:
        return self.id.generation_time

    @classmethod
    async def get_user_by_email(
        self,
        email: str
    ):
        return await self.find_one(self.email == email)

    class Collection:
        name = "users"
