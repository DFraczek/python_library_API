from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    """
    Podstawowy schemat książki, zawierający tytuł, powiązanie z książką i gatunkiem.
    """
    title: str
    author_id: int
    genre_id: int

class BookCreate(BookBase):
    """
    Schemat używany przy tworzeniu nowej książki.
    """
    pass

class BookSchema(BookBase):
    """
    Pełny schemat książki zwracany z API.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)