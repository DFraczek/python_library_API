def test_create_review_requires_authentication(client):
    """Ensure unauthenticated users cannot create reviews."""
    response = client.post(
        "/reviews/",
        json={
            "rating": 5,
            "comment": "Great book!",
            "book_id": 1,
        },
    )

    assert response.status_code == 401


def test_get_reviews_requires_authentication(client):
    """Ensure unauthenticated users cannot list reviews."""
    response = client.get("/reviews/")

    assert response.status_code == 401


def test_create_review_success(client, admin_headers, user_headers):
    """Ensure an authenticated user can create a review."""
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
            "title": "T",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    response = client.post(
        "/reviews/",
        json={
            "rating": 5,
            "comment": "Great book!",
            "book_id": book_id,
        },
        headers=user_headers,
    )

    assert response.status_code == 201
    assert response.json()["rating"] == 5


def test_user_cannot_update_another_users_review(
    client, admin_headers, user_headers, second_user_headers
):
    """Ensure a user cannot update another user's review."""
    author_id = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    ).json()["id"]

    genre_id = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    ).json()["id"]

    book_id = client.post(
        "/books/",
        json={
            "title": "T",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    ).json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 3,
            "comment": "Original review",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.put(
        f"/reviews/{review_id}",
        json={
            "rating": 1,
            "comment": "Changed by another user",
            "book_id": book_id,
        },
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_user_cannot_delete_another_users_review(
    client, admin_headers, user_headers, second_user_headers
):
    """Ensure a user cannot delete another user's review."""
    author_id = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    ).json()["id"]

    genre_id = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    ).json()["id"]

    book_id = client.post(
        "/books/",
        json={
            "title": "T",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    ).json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 3,
            "comment": "Original review",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.delete(
        f"/reviews/{review_id}",
        headers=second_user_headers,
    )

    assert response.status_code == 403


def test_admin_can_update_another_users_review(
    client, admin_headers, user_headers
):
    """Ensure an admin can update another user's review."""
    author_id = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    ).json()["id"]

    genre_id = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    ).json()["id"]

    book_id = client.post(
        "/books/",
        json={
            "title": "T",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    ).json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 3,
            "comment": "Original review",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.put(
        f"/reviews/{review_id}",
        json={
            "rating": 4,
            "comment": "Updated by admin",
            "book_id": book_id,
        },
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 4


def test_admin_can_delete_another_users_review(
    client, admin_headers, user_headers
):
    """Ensure an admin can delete another user's review."""
    author_id = client.post(
        "/authors/",
        json={"name": "A", "surname": "B"},
        headers=admin_headers,
    ).json()["id"]

    genre_id = client.post(
        "/genres/",
        json={"name": "G"},
        headers=admin_headers,
    ).json()["id"]

    book_id = client.post(
        "/books/",
        json={
            "title": "T",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    ).json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 3,
            "comment": "Original review",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.delete(
        f"/reviews/{review_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/reviews/{review_id}",
        headers=user_headers,
    )
    assert get_response.status_code == 404

def test_authenticated_user_can_get_reviews(client, user_headers):
    """Ensure an authenticated user can retrieve all reviews."""
    response = client.get(
        "/reviews/",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_user_can_update_own_review(
    client, admin_headers, user_headers
):
    """Ensure a user can update their own review."""
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
            "title": "Test Book",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 3,
            "comment": "Original review",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.put(
        f"/reviews/{review_id}",
        json={
            "rating": 5,
            "comment": "Updated review",
            "book_id": book_id,
        },
        headers=user_headers,
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 5
    assert response.json()["comment"] == "Updated review"


def test_user_can_delete_own_review(
    client, admin_headers, user_headers
):
    """Ensure a user can delete their own review."""
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
            "title": "Test Book",
            "author_id": author_id,
            "genre_id": genre_id,
        },
        headers=admin_headers,
    )
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    review_response = client.post(
        "/reviews/",
        json={
            "rating": 4,
            "comment": "Review to delete",
            "book_id": book_id,
        },
        headers=user_headers,
    )
    assert review_response.status_code == 201
    review_id = review_response.json()["id"]

    response = client.delete(
        f"/reviews/{review_id}",
        headers=user_headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/reviews/{review_id}",
        headers=user_headers,
    )
    assert get_response.status_code == 404
