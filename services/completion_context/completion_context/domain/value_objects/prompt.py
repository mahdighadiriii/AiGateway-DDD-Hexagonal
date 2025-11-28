from __future__ import annotations

from dataclasses import dataclass
from typing import Final

MAX_PROMPT_LENGTH: Final[int] = 100_000


@dataclass(frozen=True, slots=True)
class Prompt:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Prompt cannot be empty")

        if len(self.value) > MAX_PROMPT_LENGTH:
            raise ValueError("Prompt is too long")

        if self.value.isspace():
            raise ValueError("Prompt cannot be only spaces")

    def estimated_tokens(self) -> int:
        return max(3, len(self.value) // 4 + 1)

    def __str__(self) -> str:
        if len(self.value) <= 80:
            return self.value
        return self.value[:77] + "..."

    def __repr__(self) -> str:
        return f"Prompt({self.value!r})"
