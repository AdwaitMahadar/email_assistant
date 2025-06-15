import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe  # ✅ V3 decorator

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Set up Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 1024
    }
)

def load_prompt():
    with open("prompts/extract_event.txt", "r") as f:
        return f.read()

@observe(name="extract_event_from_email")  # ✅ Langfuse v3 trace
def extract_event_from_email(email_body: str, email_id: str = None) -> dict:
    prompt_template = load_prompt()
    final_prompt = prompt_template.replace("{{email_body}}", email_body)

    try:
        response = model.generate_content(final_prompt)
        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print(f"❌ Gemini extraction failed: {e}")
        return {"type": "error", "error": str(e)}
