import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

GROQ_API_KEY= os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")