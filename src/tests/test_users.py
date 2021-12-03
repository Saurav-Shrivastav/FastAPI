import json

import pytest

import app.crud.users as crud


def test_create_user(test_app, monkeypatch):
    test_request_payload = {"username": "Test User", "password": "testpass"}
    test_response_payload = {"id": 1, "username": "Test User"}

    async def mock_post(payload):
        return 1
    
    monkeypatch.setattr(crud, "users_post", mock_post)

    response = test_app.post("/users/", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_user_invalid_json(test_app):
    response = test_app.post("/users/", data=json.dumps({"username": "Testuser"}))
    assert response.status_code == 422

    response = test_app.post("/users/", data=json.dumps({"username": "1", "password": "2"}))
    assert response.status_code == 422
