from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models import Book, Genre, Author
from app.schemas.book import BookSchema, BookCreate
from app.crud import book as crud_book

router = APIRouter()


@router.post(
    "/",
    response_model=BookSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_book(
    book: BookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Book:
    """
    Add a new book to the database.
    Check whether the specified author and genre exist.
    """
    if not db.get(Author, book.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with ID {book.author_id} does not exist",
        )

    if not db.get(Genre, book.genre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with ID {book.genre_id} does not exist",
        )

    return crud_book.create_book(db=db, book_in=book)


@router.get("/", response_model=List[BookSchema])
def get_books(db: Annotated[Session, Depends(get_db)]) -> List[Book]:
    """Retrieve all books."""
    return crud_book.get_books(db)


@router.get("/{book_id}", response_model=BookSchema)
def get_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Book:
    """
    Retrieve a book by its ID.
    Raise an error if the book does not exist.
    """
    db_book = crud_book.get_book(db, book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book with the specified ID does not exist",
        )

    return db_book


@router.delete(
    "/{book_id}",
    dependencies=[Depends(require_admin)],
)
def delete_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """
    Delete a book by its ID.
    Raise an error if the book does not exist.
    """
    db_book = crud_book.get_book(db, book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book with the specified ID does not exist",
        )

    crud_book.delete_book(db=db, db_book=db_book)

    return {"message": f"Book with ID {book_id} has been deleted"}


@router.put(
    "/{book_id}",
    response_model=BookSchema,
    dependencies=[Depends(require_admin)],
)
def update_book(
    book_id: int,
    book_in: BookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Book:
    """
    Update a book's details.
    Raise an error if the book, author, or genre does not exist.
    """
    db_book = crud_book.get_book(db, book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book with the specified ID does not exist",
        )

    if not db.get(Author, book_in.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with ID {book_in.author_id} does not exist",
        )

    if not db.get(Genre, book_in.genre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with ID {book_in.genre_id} does not exist",
        )

    return crud_book.update_book(db=db, db_book=db_book, book_in=book_in)