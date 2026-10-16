from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import Role, User
from app.schemas.user import UserCreate


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Retrieve a user by their ID."""
    return db.get(User, user_id)


def get_user_by_email(db: Session, user_email: str) -> User | None:
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == user_email).first()


def get_user_by_username(db: Session, user_username: str) -> User | None:
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == user_username).first()


def get_users(db: Session) -> list[User]:
    """Retrieve all users from the database."""
    return db.query(User).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a user with a hashed password and the default USER role."""

    existing_user = (
        db.query(User)
        .filter(
            (User.email == user_in.email)
            | (User.username == user_in.username)
        )
        .first()
    )

    if existing_user:
        raise ValueError("A user with this email or username already exists.")

    user_role = db.query(Role).filter(Role.name == "USER").first()

    if user_role is None:
        raise ValueError("Default USER role does not exist.")

    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role_id=user_role.id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user