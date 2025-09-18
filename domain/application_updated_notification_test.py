from decimal import Decimal

from domain import ApplicationUpdatedNotification, PaymentPlanRow


def test_payment_plan_row_creation():
    row = PaymentPlanRow()
    row.row_index = 1
    row.total_payment = Decimal("100.00")
    row.interest = Decimal("20.00")
    row.principal = Decimal("80.00")
    row.balance = Decimal("500.00")

    assert isinstance(row, PaymentPlanRow)
    assert row.row_index == 1
    assert row.total_payment == Decimal("100.00")
    assert row.interest == Decimal("20.00")
    assert row.principal == Decimal("80.00")
    assert row.balance == Decimal("500.00")


def test_application_updated_notification_creation():
    notif = ApplicationUpdatedNotification()
    notif.email = "test@example.com"
    notif.applicationId = 123
    notif.applicationStatus = "APPROVED"
    notif.amount = 1000
    notif.term = 12
    notif.payment_plan = []

    assert isinstance(notif, ApplicationUpdatedNotification)
    assert notif.email == "test@example.com"
    assert notif.applicationId == 123
    assert notif.applicationStatus == "APPROVED"
    assert notif.amount == 1000
    assert notif.term == 12
    assert notif.payment_plan == []


def test_payment_plan_in_notification():
    row = PaymentPlanRow()
    row.row_index = 1
    row.total_payment = Decimal("100.00")
    row.interest = Decimal("20.00")
    row.principal = Decimal("80.00")
    row.balance = Decimal("500.00")

    notif = ApplicationUpdatedNotification()
    notif.email = "user@example.com"
    notif.applicationId = 456
    notif.applicationStatus = "PENDING"
    notif.amount = 2000
    notif.term = 24
    notif.payment_plan = [row]

    assert isinstance(notif.payment_plan, list)
    assert len(notif.payment_plan) == 1
    assert isinstance(notif.payment_plan[0], PaymentPlanRow)
    assert notif.payment_plan[0].row_index == 1
