import pytest
from completion_context.completion_context.domain.value_objects.prompt import Prompt


def test_valid_prompt_works() -> None:
    p = Prompt("Hello world")
    assert str(p) == "Hello world"
    assert p.estimated_tokens() >= 2


def test_short_prompt_minimum_tokens() -> None:
    assert Prompt("Hi").estimated_tokens() == 3
    assert Prompt("Hi").estimated_tokens() == 3
    assert Prompt("a").estimated_tokens() == 3


def test_longer_prompt_has_more_tokens() -> None:
    p = Prompt("ا" * 100)
    assert p.estimated_tokens() >= 25


def test_two_same_prompts_are_equal() -> None:
    assert Prompt("Hi") == Prompt("Hi")
    assert hash(Prompt("Hi")) == hash(Prompt("Hi"))


def test_empty_or_whitespace_raises() -> None:
    with pytest.raises(ValueError):
        Prompt("")
    with pytest.raises(ValueError):
        Prompt("   \n\t  ")


def test_too_long_prompt_raises() -> None:
    with pytest.raises(ValueError):
        Prompt("ا" * 100_001)


def test_immutable() -> None:
    p = Prompt("Hi")
    with pytest.raises(AttributeError):
        p.value = "bye"
