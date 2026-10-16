def test_create_book_success(client, admin_headers):
    """Test creating a book with an existing author and genre."""
    author_response = client.post(
        "/authors/",
        json={"name": "Adam", "surname": "Mickiewicz"},
        headers=admin_headers,
    )
    assert author_response.status_code == 201
    author_id = author_response.json()["id"]

    genre_response = client.post(
        "/genres/",
        json={"name": "Poezja"},
        headers=admin_headers,
    )
    assert genre_response.status_code == 201
    genre_id = genre_response.json()["id"]

    response = client.post(
        "/books/",
        json={
            "title": "Pan Tadeusz",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Pan Tadeusz"


def test_create_book_invalid_author(client, admin_headers):
    """Test creating a book with a non-existent author."""
    genre_response = client.post(
        "/genres/",
        json={"name": "Test"},
        headers=admin_headers,
    )
    assert genre_response.status_code == 201
    genre_id = genre_response.json()["id"]

    response = client.post(
        "/books/",
        json={
            "title": "Invalid Book",
            "author_id": 9999,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "author" in response.json()["detail"].lower()


def test_update_book(client, admin_headers):
    """Test updating a book's title."""
    author_response = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    )
    assert author_response.status_code == 201
    author_id = author_response.json()["id"]

    genre_response = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    )
    assert genre_response.status_code == 201
    genre_id = genre_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "Old Title",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "New Title",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_delete_book(client, admin_headers):
    """Test deleting a book."""
    author_response = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    )
    assert author_response.status_code == 201
    author_id = author_response.json()["id"]

    genre_response = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    )
    assert genre_response.status_code == 201
    genre_id = genre_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "Book to Delete",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    response = client.delete(
        f"/books/{book_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200


def test_update_non_existent_book(client, admin_headers):
    """Test updating a book that does not exist."""
    response = client.put(
        "/books/9999",
        json={
            "title": "Non-existent Book",
            "author_id": 1,
            "genre_id": 1,
        },
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"].lower()


def test_delete_non_existent_book(client, admin_headers):
    """Test deleting a book that does not exist."""
    response = client.delete(
        "/books/9999",
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"].lower()
