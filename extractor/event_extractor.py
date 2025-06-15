import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Correctly specify the model with generation config
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 1024
    }
)

# Load the prompt template
def load_prompt():
    with open("prompts/extract_event.txt", "r") as f:
        return f.read()

# Extract structured event from email using Gemini
def extract_event_from_email(email_body: str, email_id: str = None) -> dict:
    prompt_template = load_prompt()
    final_prompt = prompt_template.replace("{{email_body}}", email_body)

    try:
        response = model.generate_content(final_prompt)
        text = response.text.strip()

        # Gemini may wrap output in code fences like ```json ... ```
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        # Parse the output into a dictionary
        event = json.loads(text)
        return event

    except Exception as e:
        print(f"❌ Gemini extraction failed: {e}")
        return {"type": "error", "error": str(e)}

# Optional test run
if __name__ == "__main__":
    email_text = "Let's meet for lunch this Friday around noon. Jacob"
    result = extract_event_from_email(email_text, "email_test")
    print(result)
