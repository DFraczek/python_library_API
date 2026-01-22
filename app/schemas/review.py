from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    """
    Podstawowy schemat recenzji zawierający ocenę, komentarz oraz powiązanie z książką.
    """
    rating: int = Field(..., ge=1, le=5, description="Ocena w skali od 1 do 5")
    comment: Optional[str] = Field(None, description="Opcjonalny komentarz do oceny")
    book_id: int

class ReviewCreate(ReviewBase):
    """
    Schemat używany przy tworzeniu nowej recenzji.
    """
    pass

class ReviewSchema(ReviewBase):
    """
    Pełny schemat recenzji zwracany przez API.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)