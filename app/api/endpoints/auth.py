from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate, UserSchema
from app.core.security import create_access_token, verify_password
from app.crud.user import get_user_by_email
from app.schemas.auth import LoginSchema
from app.schemas.token import TokenSchema
router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> UserSchema:
    """Register a new user."""

    try:
        return create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

@router.post("/login", response_model=TokenSchema)
def login_user(
    credentials: LoginSchema,
    db: Session = Depends(get_db),
) -> TokenSchema:
    """Authenticate a user and return an access token."""

    user = get_user_by_email(db, credentials.email)

    if user is None or not verify_password(
        credentials.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)

    return TokenSchema(access_token=access_token)