import pytest
from completion_context.completion_context.domain.value_objects.model_name import ModelName


def test_valid_model_names() -> None:
    valid_names = [
        "gpt-4o",
        "claude-3-opus",
        "gemini-1.5-pro",
        "llama-3-70b",
        "grok-beta",
    ]

    for name in valid_names:
        model = ModelName(name)
        assert str(model) == name
        assert repr(model) == f"ModelName('{name}')"


def test_invalid_model_name_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ModelName("gpt-999-fake")

    assert "Invalid model name" in str(exc_info.value)


def test_model_name_is_immutable() -> None:
    model = ModelName("gpt-4o")

    with pytest.raises(AttributeError):
        model.value = "something-else"


def test_two_same_model_names_are_equal() -> None:
    a = ModelName("gpt-4o")
    b = ModelName("gpt-4o")

    assert a == b
    assert hash(a) == hash(b)
    assert a is not b
