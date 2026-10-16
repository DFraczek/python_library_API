def test_create_genre(client, admin_headers):
    """Test creating a genre successfully."""
    response = client.post(
        "/genres/",
        json={"name": "Fantasy"},
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Fantasy"


def test_create_duplicate_genre(client, admin_headers):
    """Test that genre names must be unique."""
    first_response = client.post(
        "/genres/",
        json={"name": "Kryminał"},
        headers=admin_headers,
    )
    assert first_response.status_code == 201

    response = client.post(
        "/genres/",
        json={"name": "Kryminał"},
        headers=admin_headers,
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_update_genre(client, admin_headers):
    """Test updating a genre's name."""
    create_response = client.post(
        "/genres/",
        json={"name": "Sci-Fi"},
        headers=admin_headers,
    )
    assert create_response.status_code == 201
    genre_id = create_response.json()["id"]

    response = client.put(
        f"/genres/{genre_id}",
        json={"name": "Science Fiction"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Science Fiction"


def test_update_non_existent_genre(client, admin_headers):
    """Test updating a genre that does not exist."""
    response = client.put(
        "/genres/9999",
        json={"name": "Unknown Genre"},
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"].lower()


def test_delete_non_existent_genre(client, admin_headers):
    """Test deleting a genre that does not exist."""
    response = client.delete(
        "/genres/9999",
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"].lower()


def test_delete_genre_success(client, admin_headers):
    """Test deleting a genre."""
    create_response = client.post(
        "/genres/",
        json={"name": "Horror"},
        headers=admin_headers,
    )
    assert create_response.status_code == 201
    genre_id = create_response.json()["id"]

    response = client.delete(
        f"/genres/{genre_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200


def test_delete_genre_with_books_conflict(client, admin_headers):
    """Test preventing deletion of a genre assigned to existing books."""
    genre_response = client.post(
        "/genres/",
        json={"name": "Test Genre"},
        headers=admin_headers,
    )
    assert genre_response.status_code == 201
    genre_id = genre_response.json()["id"]

    author_response = client.post(
        "/authors/",
        json={"name": "Jan", "surname": "Nowak"},
        headers=admin_headers,
    )
    assert author_response.status_code == 201
    author_id = author_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "Book Required for the Test",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201

    response = client.delete(
        f"/genres/{genre_id}",
        headers=admin_headers,
    )

    assert response.status_code == 400
    assert "books" in response.json()["detail"].lower()
