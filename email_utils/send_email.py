import webbrowser
import urllib.parse
from datetime import datetime

def open_confirmation_email(event: dict, place: str = None) -> None:
    """
    Opens the user's default email app with a prefilled confirmation message
    based on the event details. Optionally includes a chosen location.
    """

    # Safely extract recipient name
    participants = event.get("participants") or []
    recipient_name = participants[0] if participants else "there"
    to = f"{recipient_name}@example.com" if recipient_name != "there" else ""

    # Subject line
    subject = f"Confirming our {event.get('title', 'meeting')}"

    # Format time
    dt_str = event.get("datetime", "TBD")
    try:
        dt = datetime.fromisoformat(dt_str)
        time_info = dt.strftime("%A at %I:%M %p")
    except:
        time_info = "the scheduled time"

    # Email body
    if recipient_name == "there":
        body = "Hey,\n\n"
    else:
        body = f"Hey {recipient_name},\n\n"

    body += f"Just confirming our {event.get('title', 'meeting')} on {time_info}.\n"

    if place:
        body += f"Let's meet at {place}.\n"
    elif event.get("location") and event["location"] not in ["TBD", "Zoom"]:
        body += f"Location: {event['location']}.\n"
    else:
        body += "Let me know if the location works for you.\n"

    body += "\nSee you soon!\n"

    # Construct mailto link
    params = {
        "subject": subject,
        "body": body
    }
    mailto = f"mailto:{to}?{urllib.parse.urlencode(params)}"

    # Launch default email app
    webbrowser.open(mailto)
