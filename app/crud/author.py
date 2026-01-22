from sqlalchemy.orm import Session
from app.models import Author
from app.schemas.author import AuthorCreate

def get_author(db: Session, author_id: int) -> Author:
    """Pobiera informacje o autorze o danym ID"""
    return db.query(Author).filter(Author.id == author_id).first()

def get_authors(db: Session) -> list[Author]:
    """Pobiera wszystkich autorów z bazy"""
    return db.query(Author).all()

def create_author(db: Session, author_in: AuthorCreate) -> Author:
    """Tworzy nowego autora"""
    db_author = Author(**author_in.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, db_author: Author, author_in: AuthorCreate) -> Author:
    """Aktualizuje istniejącego autora"""
    for key, value in author_in.model_dump().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, db_author: Author) -> None:
    """Usuwa autora z bazy"""
    db.delete(db_author)
    db.commit()