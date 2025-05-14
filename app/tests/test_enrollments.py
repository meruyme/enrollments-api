from unittest.mock import Mock

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status

from app.core.constants import EnrollmentStatus
from app.core.rabbitmq import RabbitMQProvider


def test_create_enrollment_successfully(client: TestClient, valid_enrollment: dict, monkeypatch):
    mock_publish_message = Mock()

    monkeypatch.setattr(
        RabbitMQProvider,
        "publish_message",
        mock_publish_message,
    )

    response = client.post(
        "/api/v1/enrollments/", json=valid_enrollment, auth=(pytest.admin_user, pytest.admin_password),
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["_id"] is not None
    assert data["cpf"] == valid_enrollment["cpf"]
    assert data["name"] == valid_enrollment["name"]
    assert data["age"] == valid_enrollment["age"]
    assert data["status"] == EnrollmentStatus.IN_QUEUE
    assert data["requested_at"] is not None
    assert data["requested_by"] is not None
    assert data["finished_at"] is None
    assert mock_publish_message.call_count == 1

    new_enrollment = pytest.collection.find_one({"_id": ObjectId(data["_id"])})

    assert new_enrollment is not None


def test_cant_create_enrollment_with_invalid_cpf(client: TestClient):
    invalid_enrollment = {
        "cpf": "111.111.111-11",
        "name": "Test Name",
        "age": 25,
    }
    response = client.post(
        "/api/v1/enrollments/", json=invalid_enrollment, auth=(pytest.admin_user, pytest.admin_password),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_cant_create_enrollment_if_cpf_has_open_enrollment(client: TestClient, enrollment: dict):
    enrollment_payload = {
        "name": enrollment["name"],
        "cpf": enrollment["cpf"],
        "age": enrollment["age"],
    }
    response = client.post(
        "/api/v1/enrollments/", json=enrollment_payload, auth=(pytest.admin_user, pytest.admin_password),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_enrollment_sucessfully(client: TestClient, enrollment: dict):
    response = client.get(
        f"/api/v1/enrollments/{enrollment['_id']}/", auth=(pytest.admin_user, pytest.admin_password),
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, dict)
    assert data["_id"] == enrollment["_id"]


def test_cant_get_enrollment_of_different_user(client: TestClient, enrollment: dict):
    response = client.get(
        f"/api/v1/enrollments/{enrollment['_id']}/", auth=("user", "user"),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_enrollments_sucessfully(client: TestClient, enrollment: dict):
    response = client.get(
        "/api/v1/enrollments/", auth=(pytest.admin_user, pytest.admin_password),
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["_id"] == enrollment["_id"]


def test_cant_list_enrollments_sucessfully(client: TestClient, enrollment: dict):
    response = client.get(
        "/api/v1/enrollments/", auth=("user", "user"),
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0
