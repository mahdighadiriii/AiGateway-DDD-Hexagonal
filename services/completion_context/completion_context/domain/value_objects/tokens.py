from __future__ import annotations

from dataclasses import dataclass
from typing import Final

MAX_TOKENS: Final[int] = 1_000_000


@dataclass(frozen=True, slots=True)
class Tokens:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Tokens cannot be negative")
        if self.value > MAX_TOKENS:
            raise ValueError("Tokens cannot exceed 1,000,000")

    def __add__(self, other: object) -> Tokens:
        if not isinstance(other, Tokens):
            return NotImplemented
        return Tokens(self.value + other.value)

    def __sub__(self, other: object) -> Tokens:
        if not isinstance(other, Tokens):
            return NotImplemented
        result = self.value - other.value
        if result < 0:
            raise ValueError("Token subtraction cannot result in negative value")
        return Tokens(result)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Tokens):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Tokens):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Tokens):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Tokens):
            return NotImplemented
        return self.value >= other.value

    def __repr__(self) -> str:
        return f"Tokens({self.value})"

    def __str__(self) -> str:
        return f"{self.value} tokens"
