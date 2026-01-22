from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

def get_book(db: Session, book_id: int) -> Book:
    """Pobiera informacje o książce o danym ID."""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session) -> list[Book]:
    """Pobiera wszystkie książki z bazy"""
    return db.query(Book).all()

def create_book(db: Session, book_in: BookCreate) -> Book:
    """Tworzy nową książkę."""
    db_book = Book(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: Book, book_in: BookCreate) -> Book:
    """Aktualizuje dane książki."""
    for key, value in book_in.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: Book) -> None:
    """Usuwa książkę z bazy."""
    db.delete(db_book)
    db.commit()