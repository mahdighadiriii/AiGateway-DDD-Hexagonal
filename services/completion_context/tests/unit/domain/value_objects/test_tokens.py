import pytest
from completion_context.completion_context.domain.value_objects.tokens import Tokens


def test_create_valid_tokens() -> None:
    t = Tokens(150)
    assert t.value == 150
    assert str(t) == "150 tokens"


def test_zero_tokens_allowed() -> None:
    assert Tokens(0).value == 0


def test_negative_tokens_raises_error() -> None:
    with pytest.raises(ValueError, match="negative"):
        Tokens(-5)


def test_too_many_tokens_raises_error() -> None:
    with pytest.raises(ValueError, match="exceed"):
        Tokens(1_000_001)


def test_tokens_are_immutable() -> None:
    t = Tokens(100)
    with pytest.raises(AttributeError):
        t.value = 200


def test_add_tokens() -> None:
    assert Tokens(100) + Tokens(50) == Tokens(150)


def test_subtract_tokens() -> None:
    assert Tokens(200) - Tokens(50) == Tokens(150)
    with pytest.raises(ValueError, match="negative"):
        Tokens(50) - Tokens(100)


def test_comparison() -> None:
    assert Tokens(100) < Tokens(200)
    assert Tokens(200) > Tokens(100)
    assert Tokens(100) <= Tokens(100)
    assert Tokens(100) == Tokens(100)


def test_two_same_tokens_are_equal_and_hashable() -> None:
    a = Tokens(300)
    b = Tokens(300)
    assert a == b
    assert hash(a) == hash(b)
    assert a is not b
