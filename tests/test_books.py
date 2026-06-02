import sys
import os
import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from main import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client


def test_create_book(client):
    response = client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    assert response.status_code == 201


def test_get_books(client):
    client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    response = client.get("/api/books")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_single_book(client):
    client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    response = client.get("/api/books/1")

    assert response.status_code == 200
    assert response.json["title"] == "Python"


def test_update_book(client):
    client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    response = client.put(
        "/api/books/1",
        json={
            "title": "Advanced Python",
            "author": "John Doe"
        }
    )

    assert response.status_code == 200


def test_delete_book(client):
    client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    response = client.delete("/api/books/1")

    assert response.status_code == 200


def test_book_not_found(client):
    response = client.get("/api/books/999")

    assert response.status_code == 404


def test_update_book_not_found(client):
    response = client.put(
        "/api/books/999",
        json={
            "title": "Test",
            "author": "Author"
        }
    )

    assert response.status_code == 404


def test_delete_book_not_found(client):
    response = client.delete("/api/books/999")

    assert response.status_code == 404


def test_create_book_missing_fields(client):
    response = client.post(
        "/api/books",
        json={
            "title": "Python"
        }
    )

    assert response.status_code == 400


def test_update_book_missing_fields(client):
    client.post(
        "/api/books",
        json={
            "title": "Python",
            "author": "John Doe"
        }
    )

    response = client.put(
        "/api/books/1",
        json={
            "title": "Updated"
        }
    )

    assert response.status_code == 400