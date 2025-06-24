import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_homepage(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Bodza Travels" in res.data

def test_about_page(client):
    res = client.get("/about")
    assert res.status_code == 200
    assert b"ABOUT" in res.data or b"Bodza" in res.data

def test_support_page(client):
    res = client.get("/support")
    assert res.status_code == 200

def test_recent_places(client):
    res = client.get("/recent_places")
    assert res.status_code == 200

def test_autocomplete_empty(client):
    res = client.get("/autocomplete")
    assert res.status_code == 200
    assert res.json == []

def test_results_no_city(client):
    res = client.get("/results")
    assert res.status_code == 200
    assert b"No city name provided" in res.data
