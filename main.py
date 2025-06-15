import json
from extractor.event_extractor import extract_event_from_email
from memory.event_store import EventStore
from qa.question_answerer import answer_question
from calendar_utils.event_to_ics import create_ics_event  # 🆕 Import for calendar support

# Load emails from sample JSON
def load_sample_emails(filepath="data/sample_emails.json") -> list:
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    print("📨 Loading sample emails...")
    emails = load_sample_emails()

    # Create event store
    store = EventStore()

    # Step 1: Extract events from emails
    print("🧠 Extracting events from emails...\n")
    for email in emails:
        event = extract_event_from_email(email["body"], email["id"])
        if event.get("type") != "none" and event.get("type") != "error":
            store.add_event(event, email["id"])
            print(f"✓ Extracted event from {email['id']}: {event['type']}")
        else:
            print(f"✗ No event found in {email['id']}")
    
    # Step 2: Show summary
    print("\n📋 Stored events:")
    events = store.get_events()
    for e in events:
        print("-", e)

    # Step 3: Let user ask a question
    print("\n❓ Ask the assistant a question (e.g. 'Do I have lunch this week?'):\n")
    question = input("> ")

    response = answer_question(events, question)
    print("\n💬 Assistant says:")
    print(response)

    # Step 4: Ask if user wants to create calendar event
    print()
    choice = input("📅 Do you want to create a calendar event for this? (y/n): ")

    if choice.lower().startswith("y"):
        # Try to find the most relevant event
        for event in events:
            if "datetime" in event and event["datetime"] not in ["TBD", None, ""]:
                filename = f"event_{event['type']}_{event['source_email_id']}.ics"
                create_ics_event(event, filename)
                break
        else:
            print("⚠️ No suitable event with a valid datetime found.")

if __name__ == "__main__":
    main()
