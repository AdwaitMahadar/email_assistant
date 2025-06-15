import os
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe  # Optional: for trace
from pathlib import Path

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 256
    }
)

def load_prompt():
    prompt_path = Path("prompts/classify_intent.txt")
    return prompt_path.read_text()

@observe(name="classify_user_intent")
def classify_intent(user_message: str) -> str:
    try:
        template = load_prompt()
        prompt = template.replace("{{user_message}}", user_message.strip())

        response = model.generate_content(prompt)
        intent = response.text.strip().lower()

        return intent

    except Exception as e:
        print(f"❌ Intent classification failed: {e}")
        return "new_question"  # safe fallback
