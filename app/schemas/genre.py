from pydantic import BaseModel
from typing import List, Optional

class GenreBase(BaseModel):
    """
    Podstawowy schemat gatunku, zawierający jego nazwę.
    """
    name: str

class GenreCreate(GenreBase):
    """
    Schemat używany przy tworzeniu nowego gatunku.
    """
    pass

class GenreSchema(GenreBase):
    """
    Pełny schemat gatunku zwracany przez API.
    """
    id: int

    class Config:
        from_attributes = True

class GenreWithBooks(GenreSchema):
    """
    Rozszerzony schemat gatunku, który oprócz podstawowych danych
    zawiera również listę przypisanych do niego książek.
    """
    books: List["BookSchema"] = []