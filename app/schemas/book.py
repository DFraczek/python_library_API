from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    """Base schema for a book, including its title, author, and genre references."""

    title: str
    author_id: int
    genre_id: int


class BookCreate(BookBase):
    """Schema used to create a new book."""

    pass


class BookSchema(BookBase):
    """Schema representing a book returned by the API."""

    id: int

    model_config = ConfigDict(from_attributes=True)