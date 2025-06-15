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
def answer_question(events: list, question: str) -> str:
    prompt_template = load_prompt()
    final_prompt = prompt_template \
        .replace("{{event_list}}", json.dumps(events, indent=2)) \
        .replace("{{question}}", question)

    try:
        response = model.generate_content(final_prompt)
        return response.text.strip()

    except Exception as e:
        print(f"❌ Gemini Q&A failed: {e}")
        return "Sorry, I couldn't process your question."
