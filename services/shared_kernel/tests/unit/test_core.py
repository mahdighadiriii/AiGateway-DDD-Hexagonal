from __future__ import annotations

import uuid

import pytest
from shared_kernel.shared_kernel.core import EntityId, StringId, Timestamp, UuidId


def test_entity_id_requires_non_none_value() -> None:
    with pytest.raises(ValueError):
        EntityId(value=None)


def test_entity_id_equality_and_hash() -> None:
    a = EntityId("anahita")
    b = EntityId("anahita")
    c = EntityId("mahdi")
    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert len({a, b, c}) == 2


def test_uuid_id() -> None:
    u1 = UuidId()
    u2 = UuidId()
    assert isinstance(u1.value, uuid.UUID)
    assert u1 != u2
    assert str(u1)


def test_string_id() -> None:
    s = StringId()
    assert len(s.value) == 32
    assert s.value.isalnum()


def test_timestamp() -> None:
    t1 = Timestamp.now()
    t2 = Timestamp.from_iso("2025-11-28T10:00:00Z")
    assert t1.value.tzinfo is not None
    assert "2025-11-28" in str(t2)
