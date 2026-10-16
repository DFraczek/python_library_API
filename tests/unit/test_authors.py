def test_create_author(client, admin_headers):
    """Test creating an author successfully."""
    response = client.post(
        "/authors/",
        json={
            "name": "Henryk",
            "surname": "Sienkiewicz",
            "bio": "Test biography",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201
    assert response.json()["surname"] == "Sienkiewicz"


def test_get_author_by_id(client, admin_headers, user_headers):
    """Test retrieving an author by their ID."""
    create_response = client.post(
        "/authors/",
        json={"name": "Adam", "surname": "Mickiewicz"},
        headers=admin_headers,
    )
    assert create_response.status_code == 201
    author_id = create_response.json()["id"]

    response = client.get(
        f"/authors/{author_id}",
        headers=user_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Adam"


def test_update_author(client, admin_headers):
    """Test updating an existing author's details."""
    create_response = client.post(
        "/authors/",
        json={"name": "Juliusz", "surname": "Słowacki"},
        headers=admin_headers,
    )
    assert create_response.status_code == 201
    author_id = create_response.json()["id"]

    update_data = {
        "name": "Juliusz",
        "surname": "Nowak",
        "bio": "Updated biography",
    }
    response = client.put(
        f"/authors/{author_id}",
        json=update_data,
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["surname"] == "Nowak"
    assert response.json()["bio"] == "Updated biography"


def test_delete_author(client, admin_headers, user_headers):
    """Test deleting an author."""
    create_response = client.post(
        "/authors/",
        json={"name": "Adam", "surname": "Mickiewicz"},
        headers=admin_headers,
    )
    assert create_response.status_code == 201
    author_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/authors/{author_id}",
        headers=admin_headers,
    )

    assert delete_response.status_code == 200

    response = client.get(
        f"/authors/{author_id}",
        headers=user_headers,
    )
    assert response.status_code == 404

def test_delete_non_existent_author(client, admin_headers):
    """Test deleting an author that does not exist."""
    response = client.delete(
        "/authors/9999",
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]