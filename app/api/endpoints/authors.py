from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.models.book import Book
from app.models.author import Author

from app.core.database import get_db
from app.schemas.author import AuthorSchema, AuthorCreate
from app.crud import author as crud_author

router = APIRouter()

@router.post("/", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
def create_author(
    author: AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
) -> Author:
    """
    Tworzy nowy rekord autora w bazie danych.
    """
    return crud_author.create_author(db=db, author_in=author)

@router.get("/", response_model=List[AuthorSchema])
def get_authors(
    db: Annotated[Session, Depends(get_db)]
) -> List[Author]:
    """
    Pobiera listę wszystkich autorów.
    """
    return crud_author.get_authors(db)

@router.get("/{author_id}", response_model=AuthorSchema)
def get_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> Author:
    """
    Pobiera dane autora na podstawie jego ID.
    Zwraca błąd, jeśli autor o podanym ID nie istnieje.
    """
    db_author = crud_author.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor o podanym ID nie istnieje")
    return db_author

@router.put("/{author_id}", response_model=AuthorSchema)
def update_author(
    author_id: int,
    author_in: AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
) -> Author:
    """
    Aktualizuje dane istniejącego autora.
    Zwraca błąd, jeśli autor o podanym ID nie istnieje.
    """
    db_author = crud_author.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor o podanym ID nie istnieje")
    return crud_author.update_author(db=db, db_author=db_author, author_in=author_in)

@router.delete("/{author_id}")
def delete_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    """
    Usuwa autora z bazy danych (jeżeli nie ma do niego przypisanych żadnych książek).
    Zwraca błąd, jeśli autor o podanym ID nie istnieje.
    """
    db_author = crud_author.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor o podanym ID nie istnieje")

    if db.query(Book).filter(Book.author_id == author_id).first():
        raise HTTPException(
            status_code=400,
            detail="Błąd usuwania. W bazie istnieją książki przypisane do tego autora."
        )

    crud_author.delete_author(db=db, db_author=db_author)
    return {"message": f"Autor o ID {author_id} został usunięty"}