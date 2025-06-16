# loom_script.md

Hey there! I’m excited to walk you through the Email Context-Aware Assistant I built for this challenge.

---

## 🔧 What I Chose to Focus On

I decided to focus on the "automatically creating calendar events/invitations from email threads" idea. But I wanted to go a bit beyond — not just extract events, but also **understand and interact with them conversationally**.

So the assistant I built can:
- Extract events like flights, meetings, and hotel bookings from incoming emails.
- Let the user ask natural-language questions like “Do I have lunch plans?” or “When’s my next flight?”
- Create `.ics` calendar files directly.
- And even do smart actions like **send confirmation emails** or **find nearby restaurants** using Google Maps.

---

## 🧠 How I Approached the Challenge

I treated this as a modular assistant, where:
1. Emails are parsed for structured events.
2. A memory layer stores those events.
3. A conversational interface answers questions and suggests actions.
4. Actions are powered by APIs like Google Maps and Gemini.

I prioritized building a clean codebase with clearly separated modules: one for extraction, one for reasoning, one for actions, and one for intent detection.

---

## 🗂 Codebase Overview

Here’s a quick rundown of the major parts:

- `extractor/event_extractor.py`: Uses Gemini to extract structured event data from raw email bodies.
- `memory/event_store.py`: A lightweight in-memory store for managing parsed events.
- `qa/question_answerer.py`: Handles user questions using Gemini and refers to stored events.
- `calendar_utils/event_to_ics.py`: Converts events into `.ics` files the user can add to their calendar.
- `email_utils/send_email.py`: Opens a draft email to confirm meetings.
- `location_utils/nearby_finder.py`: Uses Google Maps Places and Geocoding APIs to recommend nearby places.
- `intent/classifier.py`: Classifies follow-up user commands like “create calendar event” or “send email”.
- `intent/place_parser.py`: Parses queries like “Find restaurants near Palo Alto” — this can now use either regex or an LLM.

All LLM calls are observable via **Langfuse**, and I’ve added tracing for the major functions.

---

## 🧪 How It Works (Live Demo Plan)

When the app runs:
- It loads sample emails from JSON and extracts events using Gemini.
- I can ask it questions like:
  - “When is my flight?”
  - “Do I have a meeting on Monday?”
  - “Summarize my week.”
- Based on the last question, it can offer actions:
  - Create a calendar file
  - Send a confirmation email
  - Recommend coffee shops near the event location
- For nearby place search, it uses **Google Maps APIs** with real-time geocoding + nearby search.

---

## 🧱 Problems I Encountered

**1. Gemini's API blocking:**  
Initially, I got 403 errors from Gemini. It turned out I needed to explicitly enable the `generativelanguage.googleapis.com` API and update my API key permissions.

**2. Handling bad JSON from LLM:**  
Sometimes Gemini didn’t return clean JSON. I solved this by writing a fallback retry logic that gently reminded the model to output only valid JSON.

**3. Nearby Place Extraction:**  
Extracting both the **location** and the **place type** from vague queries like “Find something near downtown” was tricky. Regex was too rigid, so I added an **LLM-based fallback parser**.

**4. Calendar events were always generated for the wrong event:**  
That was due to the assistant not remembering which event the last question referred to. I fixed that by storing the last `referenced_email_id` returned by Gemini and using it when the user asked to take an action.

---

## 🧭 Thought Process

I wanted the assistant to feel **natural** and **useful**, but not overbuilt. So I scoped down to:
- A focused set of event types.
- Clear, testable modules.
- Real-world APIs (Google Maps, Gemini, Langfuse).

I also made sure that everything could be extended easily — like replacing Gemini with another model or storing events in a database.

---

## 🌱 Future Additions

If I had more time, I’d love to:
- Add support for **email threads** and replies.
- Let users reply with “Yes/No” directly from confirmation emails.
- Store events to a **calendar app or database**.
- Add **voice input** for even more natural interaction.

---

Thanks so much for reviewing this! I had a lot of fun building it — and I hope this gives you a good sense of how I approach engineering challenges.
