import pytest
from completion_context.domain.value_objects.model_name import ModelName


def test_valid_model_names() -> None:
    valid_names = [
        "gpt-40",
        "claude-3-opus",
        "gemini-1.5-pro",
        "llama-3-70b",
        "grok-beta",
    ]

    for name in valid_names:
        model = ModelName(name)
        assert str(model) == name
        assert repr(model) == f"ModelName({name})"


def test_invalid_model_names() -> None:
    with pytest.raises(ValueError) as exc_info:
        ModelName("gpt")

    assert "Invalid model name: invalid_model_name" in str(exc_info.value)


def test_model_immutable() -> None:
    model = ModelName("gpt-40")
    with pytest.raises(AttributeError):
        model.value = "claude"


def test_two_same_model_are_equal() -> None:
    a = ModelName["gpt-40"]
    b = ModelName["gpt-40"]

    assert a == b
    assert hash(a) == hash(b)
    assert a is not b
