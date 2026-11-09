from fastapi import FastAPI

app = FastAPI(title="ResolveAI")

@app.get("/")
def root():
    return {"message": "ResolveAI is running"}