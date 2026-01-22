from sqlalchemy.orm import Session
from app.models import Genre
from app.schemas.genre import GenreCreate

def get_genre(db: Session, genre_id: int) -> Genre:
    """Pobiera informacje o gatunku o danym ID."""
    return db.get(Genre, genre_id)

def get_genres(db: Session) -> list[Genre]:
    """Pobiera wszystkie gatunki z bazy."""
    return db.query(Genre).all()

def create_genre(db: Session, genre_in: GenreCreate) -> Genre:
    """Tworzy nowy gatunek."""
    db_genre = Genre(name=genre_in.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_genre(db: Session, db_genre: Genre, genre_in: GenreCreate) -> Genre:
    """Aktualizuje nazwę gatunku."""
    db_genre.name = genre_in.name
    db.commit()
    db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, db_genre: Genre) -> None:
    """Usuwa gatunek z bazy."""
    db.delete(db_genre)
    db.commit()