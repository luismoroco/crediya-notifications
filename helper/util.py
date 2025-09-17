from decimal import ROUND_HALF_UP, Decimal


def round_decimal(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
