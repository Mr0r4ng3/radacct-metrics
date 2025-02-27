from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    full_name: Annotated[str, Field(max_length=100, examples=["John Doe"])]
    username: Annotated[str, Field(max_length=100, examples=["johndoe"])]


class UserCreate(UserBase):
    password: Annotated[str, Field(max_length=255)]


class UserPublic(UserBase):
    id: int
    is_active: bool

    @property
    def disabled(self) -> bool:
        return not self.is_active
