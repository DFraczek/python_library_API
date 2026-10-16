from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models import Book, Author
from app.schemas.author import AuthorSchema, AuthorCreate
from app.crud import author as crud_author

router = APIRouter()

@router.post(
    "/",
    response_model=AuthorSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_author(
    author: AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Author:
    """Create a new author in the database."""
    return crud_author.create_author(db=db, author_in=author)


@router.get("/", response_model=List[AuthorSchema])
def get_authors(
    db: Annotated[Session, Depends(get_db)],
) -> List[Author]:
    """Retrieve all authors."""
    return crud_author.get_authors(db)


@router.get("/{author_id}", response_model=AuthorSchema)
def get_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Author:
    """
    Retrieve an author by their ID.
    Raise an error if the author does not exist.
    """
    db_author = crud_author.get_author(db, author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author with the specified ID does not exist",
        )

    return db_author


@router.put(
    "/{author_id}",
    response_model=AuthorSchema,
    dependencies=[Depends(require_admin)],
)
def update_author(
    author_id: int,
    author_in: AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Author:
    """
    Update an existing author's details.
    Raise an error if the author does not exist.
    """
    db_author = crud_author.get_author(db, author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author with the specified ID does not exist",
        )

    return crud_author.update_author(
        db=db,
        db_author=db_author,
        author_in=author_in,
    )


@router.delete(
    "/{author_id}",
    dependencies=[Depends(require_admin)],
)
def delete_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """
    Delete an author if no books are associated with them.
    Raise an error if the author does not exist or has associated books.
    """
    db_author = crud_author.get_author(db, author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author with the specified ID does not exist",
        )

    if db.query(Book).filter(Book.author_id == author_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this author because books are associated with them.",
        )

    crud_author.delete_author(db=db, db_author=db_author)

    return {"message": f"Author with ID {author_id} has been deleted"}