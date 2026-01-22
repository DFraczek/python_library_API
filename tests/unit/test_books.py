def test_create_book_success(client):
    """Testuje poprawne utworzenie książki z istniejącym autorem i gatunkiem."""
    a_id = client.post("/authors/", json={"name": "Adam", "surname": "Mickiewicz"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "Poezja"}).json()["id"]

    response = client.post("/books/", json={
        "title": "Pan Tadeusz",
        "author_id": a_id,
        "genre_id": g_id
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Pan Tadeusz"


def test_create_book_invalid_author(client):
    """Testuje błąd przy próbie przypisania ksiazki do nieistniejącego autora."""
    g_id = client.post("/genres/", json={"name": "Test"}).json()["id"]

    response = client.post("/books/", json={
        "title": "Błędna książka",
        "author_id": 9999,
        "genre_id": g_id
    })
    assert response.status_code == 404
    assert "Autor" in response.json()["detail"]


def test_update_book(client):
    """Testuje edycję tytułu książki."""
    a_id = client.post("/authors/", json={"name": "A", "surname": "B"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "G"}).json()["id"]
    b_id = client.post("/books/", json={"title": "Stary Tytuł", "author_id": a_id, "genre_id": g_id}).json()["id"]

    response = client.put(f"/books/{b_id}", json={
        "title": "Nowy Tytuł",
        "author_id": a_id,
        "genre_id": g_id
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Nowy Tytuł"


def test_delete_book(client):
    """Testuje usunięcie książki."""
    a_id = client.post("/authors/", json={"name": "A", "surname": "B"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "G"}).json()["id"]
    b_id = client.post("/books/", json={"title": "Do usunięcia", "author_id": a_id, "genre_id": g_id}).json()["id"]

    response = client.delete(f"/books/{b_id}")
    assert response.status_code == 200

def test_update_non_existent_book(client):
    """Testuje próbę edycji książki, która nie istnieje"""
    response = client.put("/books/9999", json={
        "title": "Nieistniejąca",
        "author_id": 1,
        "genre_id": 1
    })
    assert response.status_code == 404
    assert "nie istnieje" in response.json()["detail"]

def test_delete_non_existent_book(client):
    """Testuje próbę usunięcia książki, która nie istnieje"""
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert "nie istnieje" in response.json()["detail"]