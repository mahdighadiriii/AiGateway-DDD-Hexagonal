from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .core import EntityId, Timestamp


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    occurred_at: Timestamp = field(default_factory=Timestamp.now)

    def _extra_dict_fields(self) -> dict[str, Any]:
        return {}

    def dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key == "occurred_at":
                continue
            if isinstance(value, (EntityId | Timestamp)):
                data[key] = str(value)
            elif hasattr(value, "value"):
                data[key] = value.value
            else:
                data[key] = value

        data.update(self._extra_dict_fields())
        data["event_type"] = self.__class__.__name__
        data["occurred_at"] = str(self.occurred_at)
        return data
