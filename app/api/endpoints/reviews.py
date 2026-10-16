
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import Book, Review, User
from app.schemas.review import ReviewSchema, ReviewCreate
from app.crud import review as crud_review

router = APIRouter()


@router.post(
    "/",
    response_model=ReviewSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    review: ReviewCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Review:
    """Create a review for an existing book."""

    if not db.get(Book, review.book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified book does not exist.",
        )

    return crud_review.create_review(
        db=db,
        review_in=review,
        user_id=current_user.id,
    )


@router.get("/", response_model=list[ReviewSchema])
def get_reviews(
    db: Annotated[Session, Depends(get_db)],
) -> list[Review]:
    """Retrieve all reviews."""

    return crud_review.get_reviews(db)


@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(
    review_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Review:
    """Retrieve a review by its ID."""

    db_review = crud_review.get_review(db, review_id)

    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified review does not exist.",
        )

    return db_review


@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review_in: ReviewCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Review:
    """Update a review owned by the current user or any review as an admin."""

    db_review = crud_review.get_review(db, review_id)

    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified review does not exist.",
        )

    if db_review.user_id != current_user.id and current_user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own reviews.",
        )

    if not db.get(Book, review_in.book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified book does not exist.",
        )

    return crud_review.update_review(
        db=db,
        db_review=db_review,
        review_in=review_in,
    )


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
def delete_review(
    review_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    """Delete a review owned by the current user or any review as an admin."""

    db_review = crud_review.get_review(db, review_id)

    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified review does not exist.",
        )

    if db_review.user_id != current_user.id and current_user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews.",
        )

    crud_review.delete_review(db=db, db_review=db_review)

    return {"message": f"Review {review_id} deleted successfully."}
