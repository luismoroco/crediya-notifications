from decimal import Decimal
from typing import List, ClassVar

from domain import ApplicationUpdatedNotification, ApplicationStatus, PaymentPlanRow
from domain.gateway import NotificationProvider
from helper import round_decimal
from infrastructure import SesNotificationProvider
from usecase.dto import ApplicationUpdatedDTO


class LoanNotificationUseCase:

    __MINIMUM_VALUE: ClassVar[Decimal] = Decimal("0.00")

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
        notification.payment_plan = []

        if notification.applicationStatus == ApplicationStatus.APPROVED.name:
            notification.payment_plan = self._build_payment_plan(dto=dto)

        self.notification_provider.notify_application_updated(notification)

    def _build_payment_plan(self, dto: ApplicationUpdatedDTO) -> List[PaymentPlanRow]:
        principal = Decimal(dto.amount)
        monthly_rate = dto.interestRate
        periods = dto.deadline

        installment = self._get_monthly_installment(principal, monthly_rate, periods)

        balance = principal
        plan: List[PaymentPlanRow] = []

        for k in range(1, periods + 1):
            interest = round_decimal(balance * monthly_rate)
            principal_payment = round_decimal(installment - interest)
            balance = round_decimal(balance - principal_payment)

            payment_row = PaymentPlanRow()
            payment_row.row_index = k
            payment_row.total_payment = installment
            payment_row.interest = interest
            payment_row.principal = principal_payment
            payment_row.balance = max(balance, self.__MINIMUM_VALUE)

            plan.append(payment_row)

        return plan

    @staticmethod
    def _get_monthly_installment(p: Decimal, i: Decimal, n: int) -> Decimal:
        if i == 0:
            result = p / n
        else:
            numerator = p * i
            denominator = Decimal(1) - (Decimal(1) + i) ** (-n)
            result = numerator / denominator

        return round_decimal(result)
