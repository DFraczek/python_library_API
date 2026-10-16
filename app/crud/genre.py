from sqlalchemy.orm import Session

from app.models import Genre
from app.schemas.genre import GenreCreate


def get_genre(db: Session, genre_id: int) -> Genre:
    """Retrieve a genre by ID."""
    return db.get(Genre, genre_id)


def get_genres(db: Session) -> list[Genre]:
    """Retrieve all genres from the database."""
    return db.query(Genre).all()


def create_genre(db: Session, genre_in: GenreCreate) -> Genre:
    """Create a new genre."""
    db_genre = Genre(name=genre_in.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def update_genre(
    db: Session,
    db_genre: Genre,
    genre_in: GenreCreate,
) -> Genre:
    """Update a genre's name."""
    db_genre.name = genre_in.name
    db.commit()
    db.refresh(db_genre)
    return db_genre


def delete_genre(db: Session, db_genre: Genre) -> None:
    """Delete a genre from the database."""
    db.delete(db_genre)
    db.commit()
