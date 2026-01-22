def test_create_review_success(client):
    """Testuje poprawne dodanie recenzji do książki."""
    a_id = client.post("/authors/", json={"name": "A", "surname": "B"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "G"}).json()["id"]
    b_id = client.post("/books/", json={"title": "T", "author_id": a_id, "genre_id": g_id}).json()["id"]

    response = client.post("/reviews/", json={
        "rating": 5,
        "comment": "Świetna książka!",
        "book_id": b_id
    })
    assert response.status_code == 201
    assert response.json()["rating"] == 5

def test_review_rating_validation_too_high(client):
    """
    Testuje walidację oceny ksiazki.
    Próba dodania za wysokiej oceny
    """
    response = client.post("/reviews/", json={
        "rating": 6,
        "comment": "Za wysoka ocena",
        "book_id": 1
    })
    assert response.status_code == 422

def test_review_rating_validation_too_low(client):
    """
    Testuje walidację oceny ksiazki.
    Próba dodania za niskiej oceny
    """
    response = client.post("/reviews/", json={
        "rating": 0,
        "comment": "Za niska ocena",
        "book_id": 1
    })
    assert response.status_code == 422


def test_delete_review_success(client):
    """Testuje usuniecie recenzji."""
    a_id = client.post("/authors/", json={"name": "A", "surname": "B"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "G"}).json()["id"]
    b_id = client.post("/books/", json={"title": "T", "author_id": a_id, "genre_id": g_id}).json()["id"]
    r_id = client.post("/reviews/", json={"rating": 3, "comment": "Ok", "book_id": b_id}).json()["id"]

    response = client.delete(f"/reviews/{r_id}")
    assert response.status_code == 200


def test_update_non_existent_review(client):
    """Testuje edycję nieistniejącej recenzji."""
    response = client.put("/reviews/9999", json={
        "rating": 4,
        "comment": "Błąd",
        "book_id": 1
    })
    assert response.status_code == 404


def test_cascade_delete_book_removes_reviews(client):
    """
    Testuje kaskadowe usuwanie recenzji.
    Usuniecie ksiazki spowoduje usuniecie recenzji z nią powiązanych.
    """
    a_id = client.post("/authors/", json={"name": "A", "surname": "B"}).json()["id"]
    g_id = client.post("/genres/", json={"name": "G"}).json()["id"]
    b_id = client.post("/books/", json={"title": "Do usunięcia", "author_id": a_id, "genre_id": g_id}).json()["id"]

    r_response = client.post("/reviews/", json={
        "rating": 5,
        "comment": "Recenzja zostanie usunieta razem z ksiazka",
        "book_id": b_id
    })
    r_id = r_response.json()["id"]

    client.delete(f"/books/{b_id}")

    response = client.get(f"/reviews/{r_id}")
    assert response.status_code == 404