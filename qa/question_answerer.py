import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load env vars
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
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

# Load the Q&A prompt
def load_prompt():
    with open("prompts/answer_event.txt", "r") as f:
        return f.read()

def answer_question(events: list, question: str) -> str:
    try:
        # Prepare prompt
        prompt_template = load_prompt()
        final_prompt = prompt_template \
            .replace("{{event_list}}", json.dumps(events, indent=2)) \
            .replace("{{question}}", question)

        response = model.generate_content(final_prompt)
        return response.text.strip()

    except Exception as e:
        print(f"❌ Failed to answer question: {e}")
        return "Sorry, I couldn't process your question."
