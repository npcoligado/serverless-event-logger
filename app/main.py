from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
async def create_event(event_request: EventRequest) -> EventResponse:
    """
    Create a new event.

    Parameters:
        - event_request: The event request data.

    Returns:
        The created event.
    """
    print(f"Received request: {event_request}")
    created_event = EventService.create(event_request.model_dump())

    return created_event


@app.get("/events/{id}", response_model=EventResponse)
async def get_event(id: str) -> EventResponse:
    """
    Get an event by its ID.

    Parameters:
        - id: The ID of the event.

    Returns:
        The event with the specified ID.
    """
    print(f"Retrieving details for event ID: {id}")
    event = EventService.get(id)

    if event is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Event not found"},
        )

    return event


handler = Mangum(app)
