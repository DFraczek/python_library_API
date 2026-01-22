def test_create_author(client):
    """Testuje poprawne utworzenie autora"""
    response = client.post("/authors/", json={"name": "Henryk", "surname": "Sienkiewicz", "bio": "Testowe bio"})
    assert response.status_code == 201
    assert response.json()["surname"] == "Sienkiewicz"

def test_get_author_by_id(client):
    """Testuje pobranie konkretnego autora po jego ID"""
    author_id = client.post("/authors/", json={"name": "Adam", "surname": "Mickiewicz"}).json()["id"]
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Adam"

def test_update_author(client):
    """Testuje edycję danych istniejącego autora."""
    author_id = client.post("/authors/", json={"name": "Juliusz", "surname": "Słowacki"}).json()["id"]

    update_data = {"name": "Juliusz", "surname": "Nowak", "bio": "Zmienione bio"}
    response = client.put(f"/authors/{author_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["surname"] == "Nowak"
    assert response.json()["bio"] == "Zmienione bio"


def test_delete_author(client):
    """Testuje usunięcie autora"""
    author_id = client.post("/authors/", json={"name": "Adam", "surname": "Mickiewicz"}).json()["id"]
    delete_response = client.delete(f"/authors/{author_id}")

    assert delete_response.status_code == 200

    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 404


def test_delete_non_existent_author(client):
    """Testuje próbę usunięcia nieistniejącego autora"""
    response = client.delete("/authors/9999")
    assert response.status_code == 404
    assert "nie istnieje" in response.json()["detail"]