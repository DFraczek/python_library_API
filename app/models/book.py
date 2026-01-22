from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    """
    Model SQLAlchemy reprezentujący książkę.

    Attributes:
        id (int): Unikalny identyfikator książki.
        title (str): Tytuł książki.
        author_id (int): Klucz obcy łączący książkę z autorem.
        genre_id (int): Klucz obcy łączący książkę z gatunkiem.
        author (Author): Obiekt relacji do modelu Author.
        genre (Genre): Obiekt relacji do modelu Genre.
        reviews (List[Review]): Lista recenzji przypisanych do tej książki.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    reviews = relationship("Review", back_populates="book")