from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.models.genre import Genre
from app.models.book import Book
from app.schemas.genre import GenreSchema, GenreCreate
from app.crud import genre as crud_genre

router = APIRouter()


@router.post("/", response_model=GenreSchema, status_code=status.HTTP_201_CREATED)
def create_genre(
        genre: GenreCreate,
        db: Annotated[Session, Depends(get_db)]
) -> Genre:
    """
    Tworzy nowy gatunek.
    Sprawdza unikalność nazwy.
    """
    existing_genre = db.query(Genre).filter(Genre.name == genre.name).first()
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gatunek o nazwie '{genre.name}' już istnieje."
        )

    return crud_genre.create_genre(db=db, genre_in=genre)

@router.get("/", response_model=List[GenreSchema])
def get_genres(
    db: Annotated[Session, Depends(get_db)]
) -> List[Genre]:
    """
    Pobiera listę wszystkich gatunków.
    """
    return crud_genre.get_genres(db)

@router.get("/{genre_id}", response_model=GenreSchema)
def get_genre(
    genre_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> Genre:
    """
    Pobiera szczegółowe informacje o gatunku na podstawie jego ID.
    Zwraca błąd, jeżeli gatunek o danym ID nie istnieje.
    """
    db_genre = crud_genre.get_genre(db, genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatunek o podanym ID nie istnieje"
        )
    return db_genre


@router.put("/{genre_id}", response_model=GenreSchema)
def update_genre(
        genre_id: int,
        genre_in: GenreCreate,
        db: Annotated[Session, Depends(get_db)]
) -> Genre:
    """
    Aktualizuje dane gatunku.
    Sprawdza unikalność nazwy.
    Zwraca błąd, jeżeli gatunek o takim ID nie istnieje.
    """
    db_genre = crud_genre.get_genre(db, genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatunek o podanym ID nie istnieje"
        )

    duplicate_genre = db.query(Genre).filter(
        Genre.name == genre_in.name,
        Genre.id != genre_id
    ).first()

    if duplicate_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gatunek o nazwie '{genre_in.name}' już istnieje."
        )

    return crud_genre.update_genre(db=db, db_genre=db_genre, genre_in=genre_in)

@router.delete("/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    """
    Usuwa gatunek z bazy danych (jeżeli nie ma do niego przypisanych żadnych książek).
    Zwraca błąd, jeżeli gatunek o danym ID nie istnieje.
    """
    db_genre = crud_genre.get_genre(db, genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatunek o podanym ID nie istnieje"
        )

    has_books = db.query(Book).filter(Book.genre_id == genre_id).first()
    if has_books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Błąd usuwania. W bazie istnieją książki przypisane do tego gatunku."
        )

    crud_genre.delete_genre(db=db, db_genre=db_genre)
    return {"message": f"Gatunek o ID {genre_id} ('{db_genre.name}') został usunięty"}