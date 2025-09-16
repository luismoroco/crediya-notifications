from domain import ApplicationUpdatedNotification
from domain.gateway import NotificationProvider
from infrastructure.SesNotificationProvider import SesNotificationProvider
from usecase.dto.ApplicationUpdatedDTO import ApplicationUpdatedDTO


class LoanNotificationUseCase:

    notification_provider: NotificationProvider

    def __init__(self):
        self.notification_provider = SesNotificationProvider()

    def notify_application_updated(self, dto: ApplicationUpdatedDTO):
        notification = ApplicationUpdatedNotification()
        notification.email = dto.email
        notification.applicationId = dto.applicationId
        notification.applicationStatus = dto.applicationStatus
        notification.amount = dto.amount
        notification.term = dto.deadline

        self.notification_provider.notify_application_updated(notification)
