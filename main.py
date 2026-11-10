from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from ai_service import generate_reply

class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True) # Remove whitespaces from beginning and end of string (Make sure whitespace is not considered as input)
    message: str = Field(min_length=1) # Makes sure it is a string and has minimum of 1 character

# Declares that a chat response must contain a text field name reply
class ChatResponse(BaseModel):
    reply: str

# Initialize the app with FastAPI
app = FastAPI(title="ResolveAI")

# Root endpoint
@app.get("/")
def root():
    return {"message": "ResolveAI is running"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_reply(request.message)
    return {"reply": reply}