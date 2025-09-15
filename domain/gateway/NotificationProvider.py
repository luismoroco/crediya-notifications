import abc

from domain import ApplicationUpdatedNotification


class NotificationProvider(abc.ABC):

    @abc.abstractmethod
    def notify_application_updated(self, notification: ApplicationUpdatedNotification) -> None:
        pass
