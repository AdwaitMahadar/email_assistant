import json
from extractor.event_extractor import extract_event_from_email
from memory.event_store import EventStore
from qa.question_answerer import answer_question
from calendar_utils.event_to_ics import create_ics_event
from intent.classifier import classify_intent
from summarizer.summarizer import summarize
from email_utils.send_email import open_confirmation_email
from location_utils.nearby_finder import find_nearby_places_v1
from intent.llm_place_parser import extract_place_query_llm as extract_place_query  # ✅ NEW


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

    last_event = None  # ✅ Track last referenced event

    while True:
        user_input = input("> ").strip()
        if not user_input:
            break

        result = answer_question(events, user_input)
        if isinstance(result, dict):
            print("\n💬 Assistant says:")
            print(result.get("answer", ""))
            referenced_id = result.get("referenced_email_id", None)
            last_event = store.get_event_by_email_id(referenced_id) if referenced_id else None
        else:
            print("\n💬 Assistant says:")
            print(result)
            last_event = None

        print("\n💡 You can continue the conversation or say things like:")
        print("   → create calendar event")
        print("   → send confirmation email")
        print("   → find nearby restaurants or coffee shops")
        print("   → summarize my week")
        print("   → or just ask something else!")

        follow_up = input("\n> ").strip()
        intent = classify_intent(follow_up)

        if intent == "exit":
            print("👋 Goodbye!")
            break

        elif intent == "create_calendar_event":
            target = last_event if last_event and "datetime" in last_event else None
            if not target:
                for e in events:
                    if "datetime" in e and e["datetime"] not in ["TBD", None, ""]:
                        target = e
                        break
            if target:
                filename = f"event_{target['type']}_{target['source_email_id']}.ics"
                create_ics_event(target, filename)
                print(f"✅ Calendar event saved as {filename}")
            else:
                print("⚠️ No suitable event with datetime found.")

        elif intent == "send_confirmation_email":
            if last_event:
                open_confirmation_email(last_event)
            else:
                lower_input = follow_up.lower()
                matched_event = None
                for event in events:
                    if event.get("type") != "meeting":
                        continue
                    if "participants" in event and any(p.lower() in lower_input for p in event["participants"]):
                        matched_event = event
                        break
                    if event.get("title") and "adwait" in lower_input and "adwait" in event["title"].lower():
                        matched_event = event
                        break
                if matched_event:
                    open_confirmation_email(matched_event)
                else:
                    print("⚠️ Couldn't find a matching meeting to confirm.")

        elif intent == "find_nearby_place":
            place_type, location = extract_place_query(follow_up)
            if not place_type or not location:
                print("⚠️ Please include location in the phrase eg: 'Find restaurants near Palo Alto'")
            else:
                try:
                    results = find_nearby_places_v1(place_type, location)
                    if not results:
                        print("😕 No places found.")
                    else:
                        print(f"\n📍 Top {len(results)} places near {location}:")
                        for i, place in enumerate(results, 1):
                            print(f"{i}. {place['name']} — {place['address']} (Rating: {place['rating']})")
                except Exception as e:
                    print(f"❌ Failed to fetch nearby places: {e}")

        elif intent == "summarize_events":
            summary = summarize(events, follow_up)
            print("\n📝 Summary:\n" + summary)

        elif intent == "new_question":
            result = answer_question(events, follow_up)
            if isinstance(result, dict):
                print("\n💬 Assistant says:")
                print(result.get("answer", ""))
                referenced_id = result.get("referenced_email_id", None)
                last_event = store.get_event_by_email_id(referenced_id) if referenced_id else None
            else:
                print("\n💬 Assistant says:")
                print(result)
                last_event = None

        else:
            print(f"🤖 Sorry, I didn’t understand what to do with: {follow_up}")

if __name__ == "__main__":
    main()
