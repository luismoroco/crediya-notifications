import pytest

from domain import ApplicationUpdatedNotification
from domain.gateway import NotificationProvider
from infrastructure.dummy_notification_provider import DummyNotificationProvider


def test_notification_provider_is_abstract():
    with pytest.raises(TypeError):
        NotificationProvider()


def test_concrete_notification_provider(monkeypatch):
    provider = DummyNotificationProvider()
    notif = ApplicationUpdatedNotification()
    notif.email = "test@example.com"
    notif.applicationId = 123
    notif.applicationStatus = "APPROVED"
    notif.amount = 1000
    notif.term = 12
    notif.payment_plan = []

    provider.notify_application_updated(notif)

    assert hasattr(provider, "last_notified")
    assert provider.last_notified is notif
    assert provider.last_notified.applicationId == 123
    assert provider.last_notified.applicationStatus == "APPROVED"
