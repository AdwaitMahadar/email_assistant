# 📬 Email Context-Aware Assistant

A smart command-line assistant that reads emails, extracts event information, and lets you **interact with it naturally** — from asking questions like "When is my next flight?" to finding restaurants near your conference.

---

## ✨ What Can It Do?

- 📥 **Parse Emails**  
  Extract structured events (meetings, flights, hotel bookings) from raw email text using Gemini.

- 💬 **Natural Language Q&A**  
  Ask questions like:
  - "Do I have lunch plans?"
  - "What are my hotel check-in times?"
  - "When is the AI conference?"

- 📅 **Create Calendar Events**  
  Generate `.ics` files from event data that you can drag into Google Calendar or Outlook.

- 📧 **Send Confirmation Emails**  
  Open a pre-filled email confirming attendance with extracted details.

- 🍽 **Find Nearby Places**  
  Use Google Maps APIs to find restaurants or coffee shops near any location.

- 🧠 **Smart Follow-Up Understanding**  
  The assistant keeps track of the last event you referenced to handle follow-ups like:
  - "Add that to my calendar"
  - "Send a confirmation email"

---

## 🗂 Project Structure

```txt
email_assistant/
├── main.py                      # 🔁 Entry point — interactive CLI assistant
├── data/
│   └── sample_emails.json       # Sample input emails
├── prompts/
│   ├── answer_event.txt         # Prompt for answering questions
│   └── classify_intent.txt      # Prompt for intent detection
├── extractor/
│   └── event_extractor.py       # Parses events using Gemini
├── memory/
│   └── event_store.py           # Stores extracted events
├── qa/
│   └── question_answerer.py     # Answers questions using Gemini
├── calendar_utils/
│   ├── event_to_ics.py          # Saves `.ics` files
│   └── saved_events/            # [Git-tracked folder, files ignored]
├── email_utils/
│   └── send_email.py            # Drafts a confirmation email
├── location_utils/
│   └── nearby_finder.py         # Calls Google Maps API
├── intent/
│   ├── classifier.py            # Classifies user follow-up intent
│   ├── place_parser.py          # Regex-based fallback location extractor
│   └── llm_place_parser.py      # LLM-based robust location parser
├── .gitignore
└── README.md
```

## ⚙️ Technologies Used
Tool / Service	Purpose
Python 3.12	Core language
Google Gemini API	Event extraction, Q&A, intent parsing
Google Maps API	Nearby place search
Langfuse	Tracing and observability
ICS.py	Calendar file generation
dotenv	API key management
requests	HTTP calls

## 🔒 Environment Variables
Create a .env file in the root folder with:

> GEMINI_API_KEY=your_gemini_api_key  
> GOOGLE_MAPS_API_KEY=your_maps_api_key  
Both keys are required for full functionality.  

## 🧪 How to Run

### 1. Install dependencies
> pip install -r requirements.txt

### 2. Add your .env file

### 3. Run the assistant
> python main.py

## 📝 Example Conversation

- summarize my week
> 💬 You have a flight from LAX to JFK, meetings about Q2 strategy, and an AI conference in SF...

- Find restaurants near San Francisco
> 📍 Top 3 places:
> 1. Zuni Café — 1658 Market St (Rating: 4.4)
> 2. Dumpling Home — 298 Gough St (Rating: 4.6)
> ...

- create a calendar event for it
> ✅ Calendar event saved as event_meeting_email_4.ics  
> 📁 Git Strategy  
All .ics files are saved to calendar_utils/saved_events/  

This folder is tracked in Git, but *.ics files are ignored using:

> calendar_utils/saved_events/*.ics  
This ensures structure is preserved, but personal event files are not committed.


## ✅ Final Notes
Total time spent: ~4–5 hours

Focused on meaningful assistant-like flow over email events

Heavy use of structured prompting + LLM tools + real APIs

Used Langfuse for full observability and prompt debugging