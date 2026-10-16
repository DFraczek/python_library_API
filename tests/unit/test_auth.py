def test_register_user_success(client):
    """Test registering a new user successfully."""
    response = client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201


def test_register_user_with_duplicate_email(client):
    """Test that registering with an existing email is rejected."""
    payload = {
        "username": "first_user",
        "email": "duplicate@example.com",
        "password": "SecurePassword123!",
    }
    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == 201

    response = client.post(
        "/auth/register",
        json={
            "username": "second_user",
            "email": "duplicate@example.com",
            "password": "AnotherPassword123!",
        },
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_register_user_with_duplicate_username(client):
    """Test that registering with an existing username is rejected."""
    payload = {
        "username": "duplicate_user",
        "email": "first@example.com",
        "password": "SecurePassword123!",
    }
    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == 201

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "email": "second@example.com",
            "password": "AnotherPassword123!",
        },
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_register_user_with_invalid_email(client):
    """Test that registering with an invalid email is rejected."""
    response = client.post(
        "/auth/register",
        json={
            "username": "invalid_email_user",
            "email": "not-an-email",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422


def test_register_user_without_required_fields(client):
    """Test that registration fails when required fields are missing."""
    response = client.post(
        "/auth/register",
        json={
            "username": "incomplete_user",
        },
    )

    assert response.status_code == 422


def test_registered_user_has_default_user_role(client, db):
    """Test that a newly registered user receives the USER role."""
    from app.models import Role, User

    response = client.post(
        "/auth/register",
        json={
            "username": "regular_user",
            "email": "regular_user@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 201

    user = db.query(User).filter(
        User.username == "regular_user"
    ).first()

    assert user is not None

    role = db.get(Role, user.role_id)
    assert role is not None
    assert role.name == "USER"


def test_registered_user_password_is_hashed(client, db):
    """Test that the user's password is stored as a hash."""
    from app.models import User
    from app.core.security import verify_password

    password = "SecurePassword123!"

    response = client.post(
        "/auth/register",
        json={
            "username": "hashed_user",
            "email": "hashed_user@example.com",
            "password": password,
        },
    )

    assert response.status_code == 201

    user = db.query(User).filter(
        User.username == "hashed_user"
    ).first()

    assert user is not None
    assert user.password_hash != password
    assert verify_password(password, user.password_hash)


def test_login_success(client):
    """Test logging in with valid credentials."""
    registration_response = client.post(
        "/auth/register",
        json={
            "username": "login_user",
            "email": "login_user@example.com",
            "password": "SecurePassword123!",
        },
    )
    assert registration_response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "login_user@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"].lower() == "bearer"


def test_login_with_incorrect_password(client):
    """Test that login fails when the password is incorrect."""
    registration_response = client.post(
        "/auth/register",
        json={
            "username": "wrong_password_user",
            "email": "wrong_password@example.com",
            "password": "SecurePassword123!",
        },
    )
    assert registration_response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong_password@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_with_nonexistent_email(client):
    """Test that login fails for an email that does not exist."""
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_with_invalid_email(client):
    """Test that login rejects an invalid email format."""
    response = client.post(
        "/auth/login",
        json={
            "email": "not-an-email",
            "password": "SecurePassword123!",
        },
    )

    assert response.status_code == 422