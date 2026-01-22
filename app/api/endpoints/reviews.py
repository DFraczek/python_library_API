from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.core.database import get_db
from app.models.book import Book
from app.models.review import Review
from app.schemas.review import ReviewSchema, ReviewCreate
from app.crud import review as crud_review

router = APIRouter()

@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Annotated[Session, Depends(get_db)]
) -> Review:
    """
    Tworzy nową recenzję dla książki o danym ID.
    Zwraca błąd, jeżeli taka książka nie istnieje
    """
    if not db.get(Book, review.book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Błąd dodawania recenzji. Książka o podanym ID nie istnieje."
        )
    return crud_review.create_review(db=db, review_in=review)

@router.get("/", response_model=List[ReviewSchema])
def get_reviews(
    db: Annotated[Session, Depends(get_db)]
) -> List[Review]:
    """
    Pobiera listę wszystkich recenzji.
    """
    return crud_review.get_reviews(db)

@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(
    review_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> Review:
    """
    Pobiera dane dotyczące recenzji o danym ID.
    Zwraca błąd, jeżeli recenzja o takim ID nie istnieje.
    """
    db_review = crud_review.get_review(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recenzja o podanym ID nie istnieje"
        )
    return db_review

@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review_in: ReviewCreate,
    db: Annotated[Session, Depends(get_db)]
) -> Review:
    """
    Edycja recenzji o danym ID.
    Zwraca błąd, jeżeli recenzja lub książka o danym ID nie istnieją.
    """
    db_review = crud_review.get_review(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recenzja o podanym ID nie istnieje"
        )

    if not db.get(Book, review_in.book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Błąd aktualizacji. Książka o podanym ID nie istnieje"
        )

    return crud_review.update_review(db=db, db_review=db_review, review_in=review_in)

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    """
    Usuwa recenzję o danym ID.
    Zwraca błąd, jeżeli recenzja o takim ID nie istnieje.
    """
    db_review = crud_review.get_review(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Błąd usuwania. Recenzja o ID {review_id} nie istnieje"
        )

    crud_review.delete_review(db=db, db_review=db_review)
    return {"message": f"Recenzja o ID {review_id} została usunięta"}