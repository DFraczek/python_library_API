from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Role(Base):
    """
    SQLAlchemy model representing a user role.

    Attributes:
        id (int): Unique identifier of the role.
        name (str): Unique name of the role (USER or ADMIN).
        users (list[User]): Users assigned to this role.
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")