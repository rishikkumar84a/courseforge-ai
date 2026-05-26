import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from backend.main import app

client = TestClient(app)

@patch("backend.api.routes.get_db")
def test_generate_endpoint_returns_course_id(mock_get_db):
    # Mock Motor Database
    mock_db = AsyncMock()
    mock_db_instance = AsyncMock()
    mock_db_instance["courses"].insert_one = AsyncMock(return_value=True)
    mock_get_db.return_value = mock_db_instance

    response = client.post("/api/courses/generate", json={"topic": "Machine Learning"})
    
    assert response.status_code == 200
    data = response.json()
    assert "course_id" in data
    assert data["status"] == "generating"

@patch("backend.api.routes.get_db")
def test_get_course_returns_full_course(mock_get_db):
    mock_db_instance = AsyncMock()
    mock_db_instance["courses"].find_one = AsyncMock(return_value={"id": "123", "topic": "ML"})
    mock_get_db.return_value = mock_db_instance

    response = client.get("/api/courses/123")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "123"
    assert data["topic"] == "ML"

@patch("backend.api.routes.get_db")
def test_delete_course_removes_from_db(mock_get_db):
    mock_db_instance = AsyncMock()
    mock_result = AsyncMock()
    mock_result.deleted_count = 1
    mock_db_instance["courses"].delete_one = AsyncMock(return_value=mock_result)
    mock_get_db.return_value = mock_db_instance

    response = client.delete("/api/courses/123")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}

@patch("backend.api.routes.get_db")
def test_delete_course_not_found(mock_get_db):
    mock_db_instance = AsyncMock()
    mock_result = AsyncMock()
    mock_result.deleted_count = 0
    mock_db_instance["courses"].delete_one = AsyncMock(return_value=mock_result)
    mock_get_db.return_value = mock_db_instance

    response = client.delete("/api/courses/notFound")
    assert response.status_code == 404
