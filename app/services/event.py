from app.models.event import Event


def create(event_dict: dict) -> Event:
    event = Event(**event_dict)
    event.save()

    return event


def get(event_id: str) -> Event:
    return Event.get(event_id)
