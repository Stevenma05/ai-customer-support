from fastapi import FastAPI
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

app = FastAPI(title="ResolveAI")

@app.get("/")
def root():
    return {"message": "ResolveAI is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {"reply": "Thanks for your message. Support is on the way."}