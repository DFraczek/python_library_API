from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Author(Base):
    """
    Model SQLAlchemy reprezentujący autora książek.

    Attributes:
        id (int): Unikalny identyfikator autora.
        name (str): Imię autora.
        surname (str): Nazwisko autora.
        bio (str): Krótka biografia (opcjonalnie).
        books (List[Book]): Relacja do książek napisanych przez tego autora.
    """
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")