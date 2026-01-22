from pydantic import BaseModel
from typing import Optional

class AuthorBase(BaseModel):
    """
    Podstawowy schemat autora zawierający imię, nazwisko oraz opcjonalną biografię
    """
    name: str
    surname: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    """
    Schemat używany przy tworzeniu nowego autora
    """
    pass

class AuthorSchema(AuthorBase):
    """
    Pełny schemat autora zwracany przez API.
    """
    id: int

    class Config:
        from_attributes = True