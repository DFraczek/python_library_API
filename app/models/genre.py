from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Genre(Base):
    """SQLAlchemy model representing a literary genre.

    Attributes:
        id (int): Unique identifier of the genre.
        name (str): Unique name of the genre.
        books (List[Book]): Relationship to books assigned to this genre.
    """

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship("Book", back_populates="genre")