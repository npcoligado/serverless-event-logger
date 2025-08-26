from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

import app.services.event as EventService

from app.schemas.event import EventRequest, EventResponse


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/events",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Event created",
            "model": EventResponse,
        },
        500: {
            "description": "Internal server error",
        },
    },
)
async def create_event(event_request: EventRequest):
    print(f"Received request: {event_request}")
    created_event = EventService.create(event_request.model_dump())

    return created_event


handler = Mangum(app)
