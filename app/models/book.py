from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Book(Base):
    """SQLAlchemy model representing a book.

    Attributes:
        id (int): Unique identifier of the book.
        title (str): Title of the book.
        author_id (int): Foreign key referencing the book's author.
        genre_id (int): Foreign key referencing the book's genre.
        author (Author): Relationship to the Author model.
        genre (Genre): Relationship to the Genre model.
        reviews (List[Review]): Reviews associated with this book.
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )