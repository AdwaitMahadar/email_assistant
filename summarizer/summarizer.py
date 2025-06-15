import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe  # ✅ Langfuse trace decorator

# Load env and configure Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

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
    with open("prompts/summarize_event.txt", "r") as f:
        return f.read()

@observe(name="summarize_events")
def summarize(events: list, question: str) -> str:
    try:
        prompt_template = load_prompt()
        filled_prompt = prompt_template \
            .replace("{{event_list}}", json.dumps(events, indent=2)) \
            .replace("{{question}}", question)

        response = model.generate_content(filled_prompt)
        return response.text.strip()

    except Exception as e:
        print(f"❌ Failed to summarize: {e}")
        return "Sorry, I couldn't generate a summary."
