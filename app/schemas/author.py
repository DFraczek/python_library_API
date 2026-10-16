from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    """Base schema for an author, including their name, surname, and optional biography."""

    name: str
    surname: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    """Schema used to create a new author."""

    pass


class AuthorSchema(AuthorBase):
    """Schema representing an author returned by the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)