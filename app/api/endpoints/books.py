from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.models.book import Book
from app.models.genre import Genre
from app.models.author import Author
from app.schemas.book import BookSchema, BookCreate
from app.crud import book as crud_book

router = APIRouter()

@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_book(
        book: BookCreate,
        db: Annotated[Session, Depends(get_db)]
) -> Book:
    """
    Dodaje nową książkę do bazy danych.
    Sprawdza, czy autor i gatunek o danym ID istnieją w bazie.
    """
    if not db.get(Author, book.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor o ID {book.author_id} nie istnieje"
        )

    if not db.get(Genre, book.genre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gatunek o ID {book.genre_id} nie istnieje"
        )

    return crud_book.create_book(db=db, book_in=book)


@router.get("/", response_model=List[BookSchema])
def get_books(db: Annotated[Session, Depends(get_db)]) -> List[Book]:
    """Pobiera listę wszystkich książek."""
    return crud_book.get_books(db)


@router.get("/{book_id}", response_model=BookSchema)
def get_book(book_id: int, db: Annotated[Session, Depends(get_db)]) -> Book:
    """
    Pobiera dane książki na podstawie jej ID.
    Zwraca błąd, jeżeli książka o danym ID nie istnieje.`
    """
    db_book = crud_book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Książka o podanym ID nie istnieje"
        )
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    """
    Usuwa książkę o danym ID.
    Zwraca błąd, jeżeli książka o danym ID nie istnieje.
    """
    db_book = crud_book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Książka o podanym ID nie istnieje"
        )

    crud_book.delete_book(db=db, db_book=db_book)
    return {"message": f"Książka o ID {book_id} została usunięta"}


@router.put("/{book_id}", response_model=BookSchema)
def update_book(
        book_id: int,
        book_in: BookCreate,
        db: Annotated[Session, Depends(get_db)]
) -> Book:
    """
    Aktualizuje dane książki.
    Zwraca błąd, jeżeli książka, autor lub gatunek o danym ID nie istnieją.
    """
    db_book = crud_book.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Książka o podanym ID nie istnieje"
        )

    if not db.get(Author, book_in.author_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor o ID {book_in.author_id} nie istnieje"
        )

    if not db.get(Genre, book_in.genre_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gatunek o ID {book_in.genre_id} nie istnieje"
        )

    return crud_book.update_book(db=db, db_book=db_book, book_in=book_in)