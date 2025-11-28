from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class EntityId(Generic[T]):
    value: T

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("EntityId value cannot be None")

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EntityId) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True, slots=True)
class UuidId(EntityId[uuid.UUID]):
    value: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True, slots=True)
class StringId(EntityId[str]):
    value: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass(frozen=True, slots=True)
class Timestamp:
    value: datetime = field(default_factory=lambda: datetime.now(UTC).replace(microsecond=0))

    @classmethod
    def now(cls) -> Timestamp:
        return cls()

    def __str__(self) -> str:
        return self.value.isoformat()

    @classmethod
    def from_iso(cls, iso_str: str) -> Timestamp:
        cleaned = iso_str.replace("Z", "+00:00")
        return cls(datetime.fromisoformat(cleaned))
