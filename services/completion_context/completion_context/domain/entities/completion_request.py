from __future__ import annotations

from dataclasses import dataclass, field

from shared_kernel import DomainEvent, Timestamp, UuidId

from ...value_objects import ModelName, Prompt, Tokens


@dataclass(frozen=True, kw_only=True)
class CompletionRequestCreated(DomainEvent):
    request_id: UuidId
    user_id: str
    model: str


@dataclass(kw_only=True)
class CompletionRequest:
    id: UuidId = field(default_factory=UuidId)
    user_id: str
    model: ModelName
    prompt: Prompt
    max_tokens: Tokens | None = None
    temperature: float = 0.7
    stream: bool = False
    created_at: Timestamp = field(default_factory=Timestamp.now)

    _events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(
        cls,
        user_id: str,
        model: ModelName,
        prompt: Prompt,
        *,
        max_tokens: Tokens | None = None,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> CompletionRequest:
        request = cls(
            user_id=user_id,
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )
        request._events.append(
            CompletionRequestCreated(
                request_id=request.id,
                user_id=user_id,
                model=model.value,
            )
        )
        return request

    def pull_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
