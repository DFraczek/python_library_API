from sqlalchemy.orm import Session

from app.models.role import Role


DEFAULT_ROLES = ["USER", "ADMIN"]


def create_default_roles(db: Session) -> None:
    """Create default roles if they do not exist."""

    for role_name in DEFAULT_ROLES:
        role = db.query(Role).filter(Role.name == role_name).first()

        if role is None:
            db.add(Role(name=role_name))

    db.commit()