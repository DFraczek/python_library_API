from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models import Genre, Book
from app.schemas.genre import GenreSchema, GenreCreate
from app.crud import genre as crud_genre

router = APIRouter()


@router.post(
    "/",
    response_model=GenreSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_genre(
    genre: GenreCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Genre:
    """
    Create a new genre.
    Check whether the genre name is unique.
    """
    existing_genre = db.query(Genre).filter(Genre.name == genre.name).first()

    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name '{genre.name}' already exists.",
        )

    return crud_genre.create_genre(db=db, genre_in=genre)


@router.get("/", response_model=List[GenreSchema])
def get_genres(
    db: Annotated[Session, Depends(get_db)],
) -> List[Genre]:
    """Retrieve all genres."""
    return crud_genre.get_genres(db)


@router.get("/{genre_id}", response_model=GenreSchema)
def get_genre(
    genre_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Genre:
    """
    Retrieve a genre by its ID.
    Raise an error if the genre does not exist.
    """
    db_genre = crud_genre.get_genre(db, genre_id)

    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre with the specified ID does not exist.",
        )

    return db_genre


@router.put(
    "/{genre_id}",
    response_model=GenreSchema,
    dependencies=[Depends(require_admin)],
)
def update_genre(
    genre_id: int,
    genre_in: GenreCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Genre:
    """
    Update a genre.
    Check whether the new name is unique and the genre exists.
    """
    db_genre = crud_genre.get_genre(db, genre_id)

    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre with the specified ID does not exist.",
        )

    duplicate_genre = (
        db.query(Genre)
        .filter(
            Genre.name == genre_in.name,
            Genre.id != genre_id,
        )
        .first()
    )

    if duplicate_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name '{genre_in.name}' already exists.",
        )

    return crud_genre.update_genre(
        db=db,
        db_genre=db_genre,
        genre_in=genre_in,
    )


@router.delete(
    "/{genre_id}",
    dependencies=[Depends(require_admin)],
)
def delete_genre(
    genre_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """
    Delete a genre if no books are associated with it.
    Raise an error if the genre does not exist or has associated books.
    """
    db_genre = crud_genre.get_genre(db, genre_id)

    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre with the specified ID does not exist.",
        )

    has_books = db.query(Book).filter(Book.genre_id == genre_id).first()

    if has_books:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this genre because books are associated with it.",
        )

    crud_genre.delete_genre(db=db, db_genre=db_genre)

    return {
        "message": f"Genre with ID {genre_id} ('{db_genre.name}') has been deleted."
    }