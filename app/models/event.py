import os

from datetime import datetime, UTC
from dyntastic import Dyntastic
from pydantic import Field


class Event(Dyntastic):
    def __table_name__():
        return os.environ["EVENTS_TABLE"]

    __hash_key__ = "id"

    id: str
    event_type: str
    payload: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
