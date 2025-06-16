📬 Email Context-Aware Assistant
A smart assistant that reads incoming emails, extracts event-related context (flights, meetings, hotel bookings, etc.), allows conversational Q&A over your schedule, and can take intelligent actions like creating calendar events, sending confirmation emails, summarizing your week, and recommending nearby restaurants or coffee shops.

Built as part of the Interaction Co. Technical Challenge — focused on showcasing thoughtful AI-assisted interactions over emails.

🧠 Core Features
1. Email Event Extraction
Parses and analyzes emails to extract structured event data (e.g. meetings, flights, hotel stays).

Uses the Gemini 1.5 Flash LLM to generate a structured representation from raw email bodies.

Each parsed event includes relevant fields like type, datetime, location, participants, etc.

Extracted events are stored in an in-memory EventStore.

2. Conversational Assistant
You can chat with the assistant in natural language, e.g.:

“Do I have any lunch meetings this week?”

“When is my flight?”

“Summarize my week.”

Responses are generated with context-awareness using Gemini and reference your stored event data.

3. Multi-turn Q&A + Action Suggestions
After answering a question, the assistant dynamically suggests what you can do next:


→ create calendar event
→ send confirmation email
→ find nearby restaurants or coffee shops
→ summarize my week
4. Smart Calendar Integration
You can say: “create a calendar event for it” after referencing an event.

Assistant saves a .ics calendar file for compatible import into any calendar app (Google, Apple, Outlook).

Saved to calendar_utils/saved_events/ (ignored in Git).

5. LLM-Based Nearby Place Finder
Users can ask: “Find restaurants near Palo Alto” or “Are there any coffee shops around San Francisco?”

Assistant parses the place type and location using an LLM-powered parser.

Google Maps Places API is used to fetch real nearby suggestions.

Top 3 places shown with name, address, and rating.

🗂️ Project Structure
email_assistant/
│
├── main.py                        # 🔁 Main loop – orchestrates interaction
├── data/sample_emails.json       # 📧 Sample email inputs
│
├── extractor/event_extractor.py  # 🧠 LLM-based email → event extraction
├── qa/question_answerer.py       # 💬 Gemini-powered contextual Q&A
├── calendar_utils/               # 📆 ICS event creation
│   └── event_to_ics.py
│   └── saved_events/             # (Calendar files saved here, gitignored)
├── email_utils/send_email.py     # 📤 Open confirmation email drafts
├── intent/
│   ├── classifier.py             # 🧭 Intent classification
│   └── place_parser.py           # 🧠 Regex-based place query extraction
│   └── llm_place_parser.py       # 🧠 LLM-based alternative parser
├── location_utils/nearby_finder.py # 📍 Google Maps API integration
├── memory/event_store.py         # 🧱 In-memory storage of extracted events
├── prompts/                      # 📝 Prompt templates for Gemini
│   ├── answer_event.txt
│   └── classify_intent.txt
├── .env                          # 🔐 API Keys (not committed)
├── .gitignore                    # 📁 Excludes .ics, .env, test files, etc.
└── README.md                     # 📖 You are here


⚙️ Technologies Used
Tool / Service	Purpose
Python 3.12	Core language
Google Gemini API	Event extraction, Q&A, intent parsing
Google Maps API	Nearby place search
Langfuse	Tracing and observability
ICS.py	Calendar file generation
dotenv	API key management
requests	HTTP calls

🔒 Environment Variables
Create a .env file in the root folder with:

GEMINI_API_KEY=your_gemini_api_key
GOOGLE_MAPS_API_KEY=your_maps_api_key
Both keys are required for full functionality.

🧪 How to Run
bash
Copy
Edit
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your .env file

# 3. Run the assistant
python main.py

📝 Example Conversation

> summarize my week
💬 You have a flight from LAX to JFK, meetings about Q2 strategy, and an AI conference in SF...

> Find restaurants near San Francisco
📍 Top 3 places:
1. Zuni Café — 1658 Market St (Rating: 4.4)
2. Dumpling Home — 298 Gough St (Rating: 4.6)
...

> create a calendar event for it
✅ Calendar event saved as event_meeting_email_4.ics
📁 Git Strategy
All .ics files are saved to calendar_utils/saved_events/

This folder is tracked in Git, but *.ics files are ignored using:

calendar_utils/saved_events/*.ics
This ensures structure is preserved, but personal event files are not committed.


✅ Final Notes
Total time spent: ~4–5 hours

Focused on meaningful assistant-like flow over email events

Heavy use of structured prompting + LLM tools + real APIs

Used Langfuse for full observability and prompt debugging