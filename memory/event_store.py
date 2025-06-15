# memory/event_store.py

class EventStore:
    def __init__(self):
        self.events = []

    def add_event(self, event: dict, email_id: str):
        """
        Add an event and tag it with the source email ID.
        """
        event["source_email_id"] = email_id
        self.events.append(event)

    def get_events(self) -> list:
        """
        Return all stored events.
        """
        return self.events

    def get_events_by_type(self, event_type: str) -> list:
        """
        Return events of a specific type (e.g., 'flight', 'meeting').
        """
        return [e for e in self.events if e.get("type") == event_type]

    def clear(self):
        """
        Clears all stored events (useful for testing).
        """
        self.events = []

    def get_event_by_email_id(self, email_id: str) -> dict | None:
        """
        Return the first event that matches the given email ID.
        """
        for event in self.events:
            if event.get("source_email_id") == email_id:
                return event
        return None

