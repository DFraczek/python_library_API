from sqlalchemy.orm import Session

from app.models import Book
from app.schemas.book import BookCreate


def get_book(db: Session, book_id: int) -> Book:
    """Retrieve a book by ID."""
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session) -> list[Book]:
    """Retrieve all books from the database."""
    return db.query(Book).all()


def create_book(db: Session, book_in: BookCreate) -> Book:
    """Create a new book."""
    db_book = Book(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(
    db: Session,
    db_book: Book,
    book_in: BookCreate,
) -> Book:
    """Update an existing book."""
    for key, value in book_in.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: Book) -> None:
    """Delete a book from the database."""
    db.delete(db_book)
    db.commit()
