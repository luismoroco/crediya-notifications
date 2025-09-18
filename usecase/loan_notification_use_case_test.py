from decimal import Decimal

import pytest

from domain import ApplicationStatus, PaymentPlanRow
from helper import round_decimal
from infrastructure.dummy_notification_provider import DummyNotificationProvider
from usecase import LoanNotificationUseCase
from usecase.dto import ApplicationUpdatedDTO


@pytest.fixture
def dto_approved():
    data = {
        "applicationId": 123,
        "amount": 1000,
        "deadline": 3,
        "applicationStatus": ApplicationStatus.APPROVED.name,
        "email": "user@example.com",
        "interestRate": Decimal("0.05"),
    }
    return ApplicationUpdatedDTO.from_dict(data)


@pytest.fixture
def dto_pending():
    data = {
        "applicationId": 124,
        "amount": 1000,
        "deadline": 3,
        "applicationStatus": ApplicationStatus.PENDING.name,
        "email": "user@example.com",
        "interestRate": Decimal("0.05"),
    }
    return ApplicationUpdatedDTO.from_dict(data)


def test_notify_application_updated_approved(dto_approved):
    dummy_provider = DummyNotificationProvider()

    usecase = LoanNotificationUseCase()
    usecase.notification_provider = dummy_provider

    notification = usecase.notify_application_updated(dto_approved)

    assert dummy_provider.last_notified is notification
    assert notification.applicationStatus == ApplicationStatus.APPROVED.name
    assert notification.payment_plan
    assert all(isinstance(row, PaymentPlanRow) for row in notification.payment_plan)


def test_notify_application_updated_pending(dto_pending):
    dummy_provider = DummyNotificationProvider()

    usecase = LoanNotificationUseCase()
    usecase.notification_provider = dummy_provider

    notification = usecase.notify_application_updated(dto_pending)

    assert dummy_provider.last_notified is notification
    assert notification.payment_plan == []


def test_get_monthly_installment_zero_interest():
    p = Decimal("1200")
    i = Decimal("0")
    n = 12

    result = LoanNotificationUseCase._get_monthly_installment(p, i, n)

    expected = round_decimal(p / n)
    assert result == expected
