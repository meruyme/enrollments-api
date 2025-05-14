from unittest.mock import Mock

import pytest
from bson import ObjectId

from app.core.age_group_api import AgeGroupAPIClient
from app.core.constants import EnrollmentStatus
from processor.processor import process_enrollment


def test_accept_enrollment(
    enrollment: dict, mock_channel, mock_method, sleepless, monkeypatch
):
    mock_age_group = Mock(
        return_value=[
            {
                "maximum_age": enrollment["age"] + 1,
                "minimum_age": enrollment["age"] - 1,
                "_id": "id",
            },
        ]
    )

    monkeypatch.setattr(
        AgeGroupAPIClient,
        "get_age_groups_by_age",
        mock_age_group,
    )

    process_enrollment(mock_channel, mock_method, {}, enrollment["_id"].encode("utf-8"))

    new_enrollment = pytest.collection.find_one({"_id": ObjectId(enrollment["_id"])})

    assert new_enrollment is not None
    assert new_enrollment["status"] == EnrollmentStatus.ACCEPTED
    assert new_enrollment["finished_at"] is not None


def test_refuse_enrollment_with_invalid_age(
    enrollment: dict, mock_channel, mock_method, sleepless, monkeypatch
):
    mock_age_group = Mock(
        return_value=[]
    )

    monkeypatch.setattr(
        AgeGroupAPIClient,
        "get_age_groups_by_age",
        mock_age_group,
    )

    process_enrollment(mock_channel, mock_method, {}, enrollment["_id"].encode("utf-8"))

    new_enrollment = pytest.collection.find_one({"_id": ObjectId(enrollment["_id"])})

    assert new_enrollment is not None
    assert new_enrollment["status"] == EnrollmentStatus.REFUSED
    assert new_enrollment["finished_at"] is not None
