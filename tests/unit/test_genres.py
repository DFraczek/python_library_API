def test_create_genre(client):
    """Testuje utworzenie nowego gatunku"""
    response = client.post("/genres/", json={"name": "Fantasy"})
    assert response.status_code == 201
    assert response.json()["name"] == "Fantasy"

def test_create_duplicate_genre(client):
    """Testuje walidację unikalności nazwy gatunku."""
    client.post("/genres/", json={"name": "Kryminał"})
    response = client.post("/genres/", json={"name": "Kryminał"})

    assert response.status_code == 400
    assert "już istnieje" in response.json()["detail"]

def test_update_genre(client):
    """Testuje edycję nazwy gatunku."""
    genre_id = client.post("/genres/", json={"name": "Sci-Fi"}).json()["id"]
    response = client.put(f"/genres/{genre_id}", json={"name": "Science Fiction"})

    assert response.status_code == 200
    assert response.json()["name"] == "Science Fiction"

def test_update_non_existent_genre(client):
    """Testuje próbę edycji gatunku, który nie istnieje."""
    response = client.put("/genres/9999", json={"name": "veuivnru"})
    assert response.status_code == 404
    assert "nie istnieje" in response.json()["detail"]

def test_delete_non_existent_genre(client):
    """Testuje próbę usunięcia gatunku, który nie istnieje."""
    response = client.delete("/genres/9999")
    assert response.status_code == 404
    assert "nie istnieje" in response.json()["detail"]

def test_delete_genre_success(client):
    """Testuje usunięcie gatunku."""
    genre_id = client.post("/genres/", json={"name": "Horror"}).json()["id"]
    response = client.delete(f"/genres/{genre_id}")
    assert response.status_code == 200

def test_delete_genre_with_books_conflict(client):
    """
    Testuje blokadę usunięcia gatunku, do którego przypisane są książki.
    """
    g_id = client.post("/genres/", json={"name": "Testowy gatunek"}).json()["id"]
    a_id = client.post("/authors/", json={"name": "Jan", "surname": "Nowak"}).json()["id"]

    client.post("/books/", json={
        "title": "Ksiazka konieczna do testu",
        "author_id": a_id,
        "genre_id": g_id
    })

    response = client.delete(f"/genres/{g_id}")
    assert response.status_code == 400
    assert "istnieją książki" in response.json()["detail"]