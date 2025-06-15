from ics import Calendar, Event
from datetime import datetime
import os


def create_ics_event(event: dict, output_path: str) -> None:
    cal = Calendar()
    e = Event()

    if event["type"] == "flight":
        title = f"Flight from {event['from']} to {event['to']} ({event['airline']})"
        start = event["departure"]
        e.name = title
        e.begin = datetime.fromisoformat(start)

    elif event["type"] == "meeting":
        e.name = event.get("title", "Meeting")
        dt = event.get("datetime")
        if dt and dt != "TBD":
            e.begin = datetime.fromisoformat(dt)
        else:
            e.begin = datetime.now()

        e.location = event.get("location", "TBD")

    else:
        print(f"⚠️ Unknown event type: {event['type']}")
        return

    cal.events.add(e)

    # Save to file
    with open(output_path, "w") as f:
        f.writelines(cal)
    print(f"✅ Saved calendar event to {output_path}")
