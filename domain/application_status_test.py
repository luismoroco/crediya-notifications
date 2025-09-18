from .application_status import ApplicationStatus


def test_enum_members_exist():
    assert ApplicationStatus.REJECTED.name == "REJECTED"
    assert ApplicationStatus.PENDING.name == "PENDING"
    assert ApplicationStatus.MANUAL_REVIEW.name == "MANUAL_REVIEW"
    assert ApplicationStatus.APPROVED.name == "APPROVED"


def test_enum_values():
    assert ApplicationStatus.REJECTED.value == 1
    assert ApplicationStatus.PENDING.value == 2
    assert ApplicationStatus.MANUAL_REVIEW.value == 3
    assert ApplicationStatus.APPROVED.value == 4


def test_access_by_value():
    assert ApplicationStatus(1) == ApplicationStatus.REJECTED
    assert ApplicationStatus(2) == ApplicationStatus.PENDING
    assert ApplicationStatus(3) == ApplicationStatus.MANUAL_REVIEW
    assert ApplicationStatus(4) == ApplicationStatus.APPROVED


def test_unique_values():
    values = [status.value for status in ApplicationStatus]
    assert len(values) == len(set(values)), "Enum values must be unique"
