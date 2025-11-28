from __future__ import annotations

from dataclasses import dataclass

from shared_kernel.shared_kernel.core import UuidId
from shared_kernel.shared_kernel.domain_events import DomainEvent


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
    user_id: UuidId
    email: str


def test_domain_event_has_timestamp_and_serializes_correctly() -> None:
    event = UserRegistered(user_id=UuidId(), email="anahita@example.com")
    data = event.dict()

    assert data["event_type"] == "UserRegistered"
    assert data["email"] == "anahita@example.com"
    assert isinstance(data["user_id"], str)
    assert "occurred_at" in data
    assert data["occurred_at"].endswith("Z") or "+" in data["occurred_at"]
