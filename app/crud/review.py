from sqlalchemy.orm import Session

from app.models import Review
from app.schemas.review import ReviewCreate


def get_review(db: Session, review_id: int) -> Review | None:
    """Retrieve a review by its ID."""
    return db.get(Review, review_id)


def get_reviews(db: Session) -> list[Review]:
    """Retrieve all reviews."""
    return db.query(Review).all()


def create_review(
    db: Session,
    review_in: ReviewCreate,
    user_id: int,
) -> Review:
    """Create a review associated with the specified user."""
    db_review = Review(
        **review_in.model_dump(),
        user_id=user_id,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(
    db: Session,
    db_review: Review,
    review_in: ReviewCreate,
) -> Review:
    """Update an existing review."""
    for key, value in review_in.model_dump().items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, db_review: Review) -> None:
    """Delete a review from the database."""
    db.delete(db_review)
    db.commit()