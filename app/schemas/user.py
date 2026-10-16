from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema used to register a new user."""

    password: str


class UserSchema(UserBase):
    """User data returned by the API."""

    id: int
    created_at: datetime
    role_id: int

    model_config = ConfigDict(from_attributes=True)