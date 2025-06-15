# langfuse_setup.py
import os
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://us.cloud.langfuse.com")
)


# print("DEBUG LANGFUSE ENV:")
# print("PUBLIC:", os.getenv("LANGFUSE_PUBLIC_KEY"))
# print("SECRET:", os.getenv("LANGFUSE_SECRET_KEY"))
# print("HOST:", os.getenv("LANGFUSE_HOST"))

