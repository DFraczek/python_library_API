from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate

def get_review(db: Session, review_id: int) -> Review:
    """Pobiera recenzje o danym ID"""
    return db.get(Review, review_id)

def get_reviews(db: Session) -> list[Review]:
    """Pobiera listę wszystkich recenzji."""
    return db.query(Review).all()

def create_review(db: Session, review_in: ReviewCreate) -> Review:
    """Tworzy nową recenzję."""
    db_review = Review(**review_in.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, db_review: Review, review_in: ReviewCreate) -> Review:
    """Aktualizuje dane istniejącej recenzji."""
    for key, value in review_in.model_dump().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, db_review: Review) -> None:
    """Usuwa recenzję z bazy danych."""
    db.delete(db_review)
    db.commit()