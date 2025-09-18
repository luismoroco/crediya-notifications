from domain import ApplicationUpdatedNotification
from domain.gateway import NotificationProvider


class DummyNotificationProvider(NotificationProvider):
    def __init__(self):
        self.last_notified = None

    def notify_application_updated(
        self, notification: ApplicationUpdatedNotification
    ) -> None:
        self.last_notified = notification
