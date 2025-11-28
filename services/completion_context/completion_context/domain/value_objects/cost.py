from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final

MICRO_CENT: Final[Decimal] = Decimal("0.000001")


@dataclass(frozen=True, slots=True)
class Cost:
    """USD cost with micro-cent precision – bank-grade Value Object"""

    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Cost cannot be negative")

        quantized = self.value.quantize(MICRO_CENT, rounding=ROUND_HALF_UP)
        if quantized != self.value:
            object.__setattr__(self, "value", quantized)

    @classmethod
    def from_dollars(cls, dollars: float | str | Decimal) -> Cost:
        return cls(Decimal(str(dollars)).quantize(MICRO_CENT, rounding=ROUND_HALF_UP))

    @classmethod
    def zero(cls) -> Cost:
        return cls(Decimal("0.000000"))

    def __add__(self, other: object) -> Cost:
        if not isinstance(other, Cost):
            return NotImplemented
        return Cost(self.value + other.value)

    def __sub__(self, other: object) -> Cost:
        if not isinstance(other, Cost):
            return NotImplemented
        result = self.value - other.value
        if result < 0:
            raise ValueError("Cost subtraction cannot result in negative value")
        return Cost(result)

    def __mul__(self, multiplier: int | float) -> Cost:
        if not isinstance(multiplier, int | float):
            return NotImplemented
        return Cost(self.value * Decimal(str(multiplier)))

    def __truediv__(self, divisor: int | float) -> Cost:
        if not isinstance(divisor, int | float) or divisor == 0:
            return NotImplemented
        return Cost(self.value / Decimal(str(divisor)))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Cost):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Cost):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Cost):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Cost):
            return NotImplemented
        return self.value >= other.value

    def __repr__(self) -> str:
        return f"Cost(${self.value})"

    def __str__(self) -> str:
        return f"${self.value:.6f}"

    def to_dollars(self) -> Decimal:
        return self.value
