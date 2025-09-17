from decimal import Decimal
from typing import List

class PaymentPlanRow:

    row_index: int
    total_payment: Decimal
    interest: Decimal
    principal: Decimal
    balance: Decimal

    def __init__(self):
        pass

class ApplicationUpdatedNotification:

    email: str
    applicationId: int
    applicationStatus: str
    amount: int
    term: int
    payment_plan: List[PaymentPlanRow]

    def __init__(self):
        pass
