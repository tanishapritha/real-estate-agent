# app/events/bus.py
"""Simple Redis Streams event bus.
Provides `publish` to write an event to a stream and `consume` generator to read events.
All events inherit from `BaseEvent` defined in `schemas.py`.
"""

import os
import json
from typing import Generator, Type, TypeVar

import redis
from redis.exceptions import ResponseError

from .schemas import BaseEvent

# Initialize Redis client from environment (fallback to localhost)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_client = redis.Redis.from_url(REDIS_URL)

T = TypeVar("T", bound=BaseEvent)


def _ensure_group(stream: str, group: str) -> None:
    """Create consumer group if it does not exist (idempotent)."""
    try:
        _client.xgroup_create(name=stream, groupname=group, mkstream=True)
    except ResponseError as e:
        # Group already exists raises BUSYGROUP; ignore it
        if "BUSYGROUP" not in str(e):
            raise


def publish(event: BaseEvent, stream: str) -> None:
    """Publish an event instance to a Redis stream.

    The event is serialized as JSON and stored under the field ``data``.
    """
    payload = event.json()
    _client.xadd(stream, {"data": payload})


def consume(event_type: Type[T], stream: str, group: str, consumer: str, count: int = 1, block: int = 0) -> Generator[T, None, None]:
    """Consume events of a specific type from a Redis stream.

    Parameters
    ----------
    event_type: Pydantic model class inheriting from ``BaseEvent``.
    stream: Name of the Redis stream.
    group: Consumer group name.
    consumer: Consumer identifier within the group.
    count: Max number of entries to return per XREADGROUP call.
    block: Milliseconds to wait for new entries (0 = no block).
    """
    _ensure_group(stream, group)
    while True:
        resp = _client.xreadgroup(groupname=group, consumername=consumer, streams={stream: ">"}, count=count, block=block)
        if not resp:
            # No messages returned – exit if non‑blocking, otherwise continue waiting
            if block == 0:
                break
            continue
        for _stream_name, messages in resp:
            for message_id, fields in messages:
                raw = fields.get(b"data")
                if raw:
                    data = json.loads(raw)
                    # Parse JSON into the given Pydantic model
                    yield event_type(**data)
        # For a simple demo we break after processing the batch
        break
