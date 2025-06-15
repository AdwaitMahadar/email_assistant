import json
from extractor.event_extractor import extract_event_from_email
from memory.event_store import EventStore
from qa.question_answerer import answer_question
from calendar_utils.event_to_ics import create_ics_event
from intent.classifier import classify_intent  # ✅ New

# Load emails from sample JSON
def load_sample_emails(filepath="data/sample_emails.json") -> list:
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    print("📨 Loading sample emails...")
    emails = load_sample_emails()

    store = EventStore()

    print("🧠 Extracting events from emails...\n")
    for email in emails:
        event = extract_event_from_email(email["body"], email["id"])
        if event.get("type") != "none" and event.get("type") != "error":
            store.add_event(event, email["id"])
            print(f"✓ Extracted event from {email['id']}: {event['type']}")
        else:
            print(f"✗ No event found in {email['id']}")

    events = store.get_events()

    print("\n📋 Stored events:")
    for e in events:
        print("-", e)

    print("\n❓ Ask the assistant a question (e.g. 'Do I have lunch this week?'):\n")

    while True:
        user_input = input("> ").strip()
        if not user_input:
            break

        response = answer_question(events, user_input)
        print("\n💬 Assistant says:")
        print(response)

        print("\n💡 You can continue the conversation or say things like:")
        print("   → create calendar event")
        print("   → send confirmation email")
        print("   → find nearby restaurants or coffee shops")
        print("   → or just ask something else!")

        follow_up = input("\n> ").strip()

        # 🔍 Use Gemini to classify intent
        intent = classify_intent(follow_up)

        if intent == "exit":
            print("👋 Goodbye!")
            break

        elif intent == "create_calendar_event":
            for event in events:
                if "datetime" in event and event["datetime"] not in ["TBD", None, ""]:
                    filename = f"event_{event['type']}_{event['source_email_id']}.ics"
                    create_ics_event(event, filename)
                    print(f"✅ Calendar event saved as {filename}")
                    break
            else:
                print("⚠️ No suitable event with datetime found.")

        elif intent == "send_confirmation_email":
            print("📧 (Placeholder) Sending confirmation email... (to be implemented)")

        elif intent == "find_nearby_place":
            print("📍 (Placeholder) Finding nearby places... (to be implemented)")

        elif intent == "new_question":
            response = answer_question(events, follow_up)
            print("\n💬 Assistant says:")
            print(response)

        else:
            print(f"🤖 Sorry, I didn’t understand what to do with: {follow_up}")

if __name__ == "__main__":
    main()
