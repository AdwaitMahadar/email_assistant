import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe  # ✅ V3 decorator

# Load env vars
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Gemini model config
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 512
    }
)

def load_prompt():
    with open("prompts/answer_event.txt", "r") as f:
        return f.read()

@observe(name="answer_question")  # ✅ Langfuse v3 trace
def answer_question(events: list, question: str) -> dict:
    prompt_template = load_prompt()
    base_prompt = prompt_template.replace("{{event_list}}", json.dumps(events, indent=2))
    final_prompt = base_prompt.replace("{{question}}", question)

    try:
        response = model.generate_content(final_prompt)
        text = response.text.strip()

        # Handle markdown-wrapped JSON
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            # Fallback: if model doesn't return clean JSON, retry with hint
            fallback_prompt = (
                final_prompt
                + "\n\nMake sure your response is a clean JSON object as described above."
            )
            fallback_response = model.generate_content(fallback_prompt)
            text = fallback_response.text.strip()
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            try:
                parsed = json.loads(text)
            except:
                parsed = {
                    "answer": "Sorry, I couldn't understand your question clearly.",
                    "referenced_email_id": "none"
                }

        referenced_id = parsed.get("referenced_email_id", "none")

        # ✅ Fallback logic if ID is missing
        if referenced_id == "none":
            question_lower = question.lower()
            matched_event = None
            for event in events:
                if event.get("type") == "flight" and "flight" in question_lower:
                    matched_event = event
                elif event.get("type") == "meeting" and any(
                    kw in question_lower for kw in ["meeting", "lunch", "dinner", "call"]
                ):
                    matched_event = event
                elif event.get("type") == "hotel" and "hotel" in question_lower:
                    matched_event = event
                if matched_event:
                    referenced_id = matched_event.get("source_email_id")
                    break

        return {
            "answer": parsed.get("answer", "Sorry, I couldn't find any answer."),
            "referenced_email_id": referenced_id
        }

    except Exception as e:
        print(f"❌ Failed to answer question: {e}")
        return {
            "answer": "Sorry, I couldn't process your question.",
            "referenced_email_id": "none"
        }
