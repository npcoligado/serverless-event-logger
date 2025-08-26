from dyntastic import DoesNotExist

from app.models.event import Event


def create(event_dict: dict) -> Event:
    event = Event(**event_dict)
    event.save()

    return event


def get(event_id: str) -> Event:
    try:
        return Event.get(event_id)
    except DoesNotExist:
        return None
