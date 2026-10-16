from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """
    SQLAlchemy model representing a library user.

    Attributes:
        id (int): Unique identifier of the user.
        username (str): Unique username of the user.
        email (str): Unique email address of the user.
        password_hash (str): Hashed password of the user.
        role_id (int): Foreign key referencing the user's role.
        created_at (datetime): Date and time when the account was created.
        role (Role): Role assigned to the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    role = relationship("Role", back_populates="users")
    reviews = relationship("Review", back_populates="user")