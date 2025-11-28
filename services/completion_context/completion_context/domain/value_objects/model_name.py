from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_VALID_MODELS: Final[set[str]] = {
    "gpt-4o",
    "claude-3-opus",
    "gemini-1.5-pro",
    "llama-3-70b",
    "grok-beta",
}


@dataclass(frozen=True, slots=True)
class ModelName:
    value: str

    def __post_init__(self) -> None:
        if self.value not in _VALID_MODELS:
            raise ValueError(f"Invalid model name: {self.value}")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"ModelName({self.value})"
