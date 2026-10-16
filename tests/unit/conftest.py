import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models import Role, User


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraints in SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Create a clean database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        session.add_all([
            Role(name="USER"),
            Role(name="ADMIN"),
        ])
        session.commit()

        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Use the test database for API requests."""

    def _get_test_db():
        yield db

    app.dependency_overrides[get_db] = _get_test_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_headers_factory(db):
    """Create a test user and return their authorization headers."""

    def create_headers(
        role_name: str,
        username: str,
    ) -> dict[str, str]:
        role = db.query(Role).filter(Role.name == role_name).first()

        if role is None:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
            db.refresh(role)

        user = User(
            username=username,
            email=f"{username}@example.com",
            password_hash=hash_password("TestPassword123!"),
            role_id=role.id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id)

        return {"Authorization": f"Bearer {token}"}

    return create_headers


@pytest.fixture
def user_headers(auth_headers_factory):
    """Return authorization headers for a regular user."""
    return auth_headers_factory("USER", "test_user")


@pytest.fixture
def second_user_headers(auth_headers_factory):
    """Return authorization headers for a second regular user."""
    return auth_headers_factory("USER", "second_user")


@pytest.fixture
def admin_headers(auth_headers_factory):
    """Return authorization headers for an administrator."""
    return auth_headers_factory("ADMIN", "test_admin")
