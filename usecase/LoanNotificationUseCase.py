from infrastructure.SESNotificationProvider import SESNotificationProvider
from usecase.dto.ApplicationUpdatedDTO import ApplicationUpdatedDTO
from domain.gateway import NotificationProvider
from domain import ApplicationUpdatedNotification

class LoanNotificationUseCase:

    notification_provider: NotificationProvider

    def __init__(self):
        self.notification_provider = SESNotificationProvider()

    def notify_application_updated(self, dto: ApplicationUpdatedDTO):
        notification = ApplicationUpdatedNotification()
        notification.email = dto.email
        notification.applicationId = dto.applicationId
        notification.applicationStatus = dto.applicationStatus
        notification.amount = dto.amount
        notification.term = dto.deadline

        self.notification_provider.notify_application_updated(notification)
