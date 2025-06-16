import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 128
    }
)

@observe(name="llm_place_parser")
def extract_place_query_llm(user_input: str) -> tuple:
    prompt = f"""
You are an assistant that extracts location-based place search queries from user input.

Given a sentence like:
"Find restaurants near Palo Alto"
"Are there coffee shops in San Francisco?"

Return JSON in this format (no explanations, just JSON):
{{
  "place_type": "restaurant",
  "location": "Palo Alto"
}}

If not sure, return:
{{"place_type": "", "location": ""}}

User input: "{user_input}"
"""

    try:
        response = model.generate_content(prompt)
        # print("🧠 Raw LLM response:", response.text)

        # Safely extract JSON block
        text = response.text.strip()

        if "```" in text:
            # Remove any markdown code fence
            text = text.split("```")[1].strip()
            if text.lower().startswith("json"):
                text = text[len("json"):].strip()

        parsed = json.loads(text)
        return parsed.get("place_type"), parsed.get("location")

    except Exception as e:
        print(f"❌ LLM place extraction failed: {e}")
        return None, None