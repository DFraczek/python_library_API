import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Review(Base):
    """
    Model SQLAlchemy reprezentujący recenzję książki.

    Attributes:
        id (int): Unikalny identyfikator recenzji.
        rating (int): Ocena w skali 1-5.
        comment (str): Treść recenzji.
        created_at (datetime): Data i godzina dodania recenzji.
        book_id (int): Klucz obcy do tabeli books.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    book = relationship("Book", back_populates="reviews")