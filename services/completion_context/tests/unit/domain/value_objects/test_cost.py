from decimal import Decimal

import pytest
from completion_context.completion_context.domain.value_objects.cost import Cost


def test_create_cost_from_dollars() -> None:
    c = Cost.from_dollars(0.02)
    assert str(c) == "$0.020000"
    assert c.to_dollars() == Decimal("0.020000")


def test_cost_is_always_six_decimal_places() -> None:
    c = Cost.from_dollars(0.1)
    assert str(c) == "$0.100000"
    c2 = Cost.from_dollars("0.123456789")
    assert str(c2) == "$0.123457"


def test_add_and_subtract_cost() -> None:
    assert Cost.from_dollars(0.02) + Cost.from_dollars(0.03) == Cost.from_dollars(0.05)
    assert Cost.from_dollars(0.10) - Cost.from_dollars(0.03) == Cost.from_dollars(0.07)


def test_negative_cost_raises_error() -> None:
    with pytest.raises(ValueError, match="negative"):
        Cost(Decimal("-0.01"))


def test_cost_comparison() -> None:
    assert Cost.from_dollars(0.01) < Cost.from_dollars(0.02)
    assert Cost.from_dollars(0.05) >= Cost.from_dollars(0.05)


def test_zero_cost() -> None:
    assert Cost.zero() == Cost.from_dollars(0)
    assert str(Cost.zero()) == "$0.000000"


def test_multiplication() -> None:
    assert Cost.from_dollars(0.02) * 150 == Cost.from_dollars(3.00)


def test_immutable_and_equal_by_value() -> None:
    a = Cost.from_dollars(0.02)
    b = Cost.from_dollars(0.02)
    assert a == b
    assert hash(a) == hash(b)
    with pytest.raises(AttributeError):
        a.value = Decimal("99.99")
