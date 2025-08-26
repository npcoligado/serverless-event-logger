from datetime import datetime
from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    id: str
    event_type: str = Field(..., alias="type")
    payload: dict


class EventResponse(EventRequest):
    class Config:
        allow_population_by_field_name = True

    created_at: datetime
