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
    base_prompt = prompt_template.replace("{{event_list}}", json.dumps(events, indent=2))
    final_prompt = base_prompt.replace("{{question}}", question)

    try:
        response = model.generate_content(final_prompt)
        answer = response.text.strip()

        if answer.lower().strip(".!?") == question.lower().strip(".!?") or len(answer.split()) < 5:
            fallback_prompt = (
                final_prompt
                + "\n\nNote: If you're unsure how to answer, ask the user to clarify or suggest what they could do next."
            )
            fallback_response = model.generate_content(fallback_prompt)
            answer = fallback_response.text.strip()

        return answer

    except Exception as e:
        print(f"❌ Failed to answer question: {e}")
        return "Sorry, I couldn't process your question."