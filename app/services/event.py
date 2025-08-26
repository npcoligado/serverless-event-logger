from app.models.event import Event


def create(event_dict: dict) -> Event:
    event = Event(**event_dict)
    event.save()

    return event
