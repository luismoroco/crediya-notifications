from decimal import Decimal

import pytest

from helper import round_decimal


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (Decimal("1.234"), Decimal("1.23")),  # redondeo hacia abajo
        (Decimal("1.235"), Decimal("1.24")),  # redondeo hacia arriba
        (Decimal("0.005"), Decimal("0.01")),  # caso borde
        (Decimal("0.004"), Decimal("0.00")),  # caso borde
        (Decimal("2.999"), Decimal("3.00")),  # redondeo al siguiente entero
        (Decimal("-1.235"), Decimal("-1.24")),  # negativos
        (Decimal("-1.234"), Decimal("-1.23")),  # negativos
    ],
)
def test_round_decimal(input_value, expected):
    result = round_decimal(input_value)
    assert result == expected
