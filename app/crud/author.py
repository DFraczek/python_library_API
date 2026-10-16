from sqlalchemy.orm import Session

from app.models import Author
from app.schemas.author import AuthorCreate


def get_author(db: Session, author_id: int) -> Author:
    """Retrieve an author by ID."""
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session) -> list[Author]:
    """Retrieve all authors from the database."""
    return db.query(Author).all()


def create_author(db: Session, author_in: AuthorCreate) -> Author:
    """Create a new author."""
    db_author = Author(**author_in.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
    db: Session,
    db_author: Author,
    author_in: AuthorCreate,
) -> Author:
    """Update an existing author."""
    for key, value in author_in.model_dump().items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, db_author: Author) -> None:
    """Delete an author from the database."""
    db.delete(db_author)
    db.commit()
