from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Author(Base):
    """SQLAlchemy model representing a book author.

    Attributes:
        id (int): Unique identifier of the author.
        name (str): Author's first name.
        surname (str): Author's last name.
        bio (str | None): Optional short biography.
        books (List[Book]): Relationship to books written by this author.
    """

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")