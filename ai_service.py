from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(message: str) -> str:
    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=(
            "You are ResolveAI, a customer support assistant. "
            "Give clear, consice help. "
            "Do not invent company policies or claim to access custimer accounts. "
        ),
        input=message,
        max_output_tokens=300,
    )
    
    return response.output_text