from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Genre(Base):
    """
    Model reprezentujący gatunek literacki.

    Attributes:
        id (int): Unikalny identyfikator gatunku.
        name (str): Unikalna nazwa gatunku.
        books (List[Book]): Relacja do książek przypisanych do tego gatunku.
    """
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship("Book", back_populates="genre")