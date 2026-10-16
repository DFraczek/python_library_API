from typing import List

from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    """Base schema for a genre, containing its name."""

    name: str


class GenreCreate(GenreBase):
    """Schema used to create a new genre."""

    pass


class GenreSchema(GenreBase):
    """Schema representing a genre returned by the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreWithBooks(GenreSchema):
    """Extended genre schema that includes its associated books."""

    books: List["BookSchema"] = []