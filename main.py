import json
from extractor.event_extractor import extract_event_from_email
from memory.event_store import EventStore
from qa.question_answerer import answer_question

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
    for e in store.get_events():
        print("-", e)

    # Step 3: Let user ask a question
    print("\n❓ Ask the assistant a question (e.g. 'Do I have lunch this week?'):\n")
    question = input("> ")

    response = answer_question(store.get_events(), question)
    print("\n💬 Assistant says:")
    print(response)

if __name__ == "__main__":
    main()
