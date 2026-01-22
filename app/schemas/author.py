from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict

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

    model_config = ConfigDict(from_attributes=True)