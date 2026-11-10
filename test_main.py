'''
from main import app imports your actual FastAPI application.
TestClient(app) creates a client that can send requests directly to it.
client.post(...) sends the same JSON request you submitted through /docs.
Each assert checks an expected result. If the result differs, the test fails.
The file and function names start with test_ so pytest can discover them.
'''

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
def test_chat_rejects_missing_message():
    response = client.post(
        "/chat", json={}
    )
    
    assert response.status_code == 422
    
def test_chat_rejects_empty_message():
    response = client.post(
        "/chat", json={"message": ""}
    )
    
    assert response.status_code == 422
    
def test_chat_rejects_whitespace_message():
    response = client.post(
        "/chat", json={"message": "   "}
    )
    
    assert response.status_code == 422
    
def test_chat_returns_reply(monkeypatch):
    def fake_generate_reply(message: str) -> str:
        assert message == "How do I reset my password?"
        return "This is a test reply."

    monkeypatch.setattr("main.generate_reply", fake_generate_reply)

    response = client.post(
        "/chat",
        json={"message": "How do I reset my password?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "reply": "This is a test reply."
    }