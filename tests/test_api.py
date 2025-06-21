import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_autocomplete_no_query(client):
    response = client.get("/autocomplete?text=")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []

def test_autocomplete_valid_query(client):
    response = client.get("/autocomplete?text=budapest")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert "features" in data
    assert isinstance(data["features"], list)

def test_results_no_city(client):
    response = client.get("/results")
    assert response.status_code == 200
    assert b"No city name provided" in response.data

def test_results_valid_city(client):
    response = client.get("/results?city=Budapest")
    assert response.status_code == 200
    assert b"Top sights in Budapest" in response.data or b"No sights found" in response.data
