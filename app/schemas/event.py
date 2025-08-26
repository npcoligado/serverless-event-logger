from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class EventRequest(BaseModel):
    id: str
    event_type: str = Field(..., alias="type")
    payload: dict


class EventResponse(EventRequest):
    model_config = ConfigDict(populate_by_name=True)

    created_at: datetime
