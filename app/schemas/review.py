from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    """Base schema for a book review."""
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating on a scale from 1 to 5",
    )
    comment: str | None = Field(
        None,
        description="Optional review comment",
    )
    book_id: int


class ReviewCreate(ReviewBase):
    """Schema used to create a new review."""
    pass


class ReviewSchema(ReviewBase):
    """Complete review schema returned by the API."""
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)