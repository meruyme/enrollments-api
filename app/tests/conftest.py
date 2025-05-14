import time
import pytest
import os

from datetime import datetime
from fastapi.testclient import TestClient

from app.core.constants import Environment, EnrollmentStatus
from app.main import app
from app.core.db import DatabaseProvider


os.environ["ENVIRONMENT"] = Environment.TEST


def pytest_configure():
    pytest.db = DatabaseProvider.get_database()
    pytest.collection = pytest.db.enrollments
    pytest.admin_user = "admin_user"
    pytest.admin_password = "admin"


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_database():
    db = DatabaseProvider.get_database()
    db.drop_collection("enrollments")
    yield
    db.drop_collection("enrollments")


@pytest.fixture
def valid_enrollment():
    return {
        "cpf": "239.965.510-96",
        "name": "Test Name",
        "age": 25,
    }


@pytest.fixture
def enrollment():
    enrollment_data = {
        "cpf": "239.965.510-96",
        "name": "Test Name",
        "age": 25,
        "status": EnrollmentStatus.IN_QUEUE,
        "requested_by": pytest.admin_user,
        "requested_at": datetime.now(),
        "finished_at": None,
    }

    enrollment = pytest.collection.insert_one(enrollment_data)

    enrollment_data.update({"_id": str(enrollment.inserted_id)})

    return enrollment_data


@pytest.fixture
def mock_channel():
    class MockChannel:
        def basic_ack(self, delivery_tag: int):
            return

        def basic_nack(self, delivery_tag: int):
            return

    return MockChannel()


@pytest.fixture
def mock_method():
    class MockMethod:
        def __init__(self, delivery_tag=1):
            self.delivery_tag = delivery_tag

    return MockMethod()


@pytest.fixture
def sleepless(monkeypatch):
    def sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", sleep)
