from app.ai_service import generate_reply
from types import SimpleNamespace

def test_generate_reply_handles_no_matches(monkeypatch):
    def fake_retrieve_policies(question: str):
        return []
    
    monkeypatch.setattr(
        "app.ai_service.retrieve_policies",
        fake_retrieve_policies
    )
    
    reply = generate_reply("Does Northstar offer a student discount?")
    
    assert reply == (
        "I couldn't find relevant policy information. "
        "Please contact support."
    )
    
def test_generate_reply_uses_retrieved_policy(monkeypatch):
    policy_text = "Northstar provides prepaid labels for defective returns."

    def fake_retrieve_policies(question: str):
        return [
            SimpleNamespace(
                metadata={
                    "source": "returns.md",
                    "text": policy_text,
                }
            )
        ]

    def fake_create(**kwargs):
        assert policy_text in kwargs["input"]
        assert "returns.md" in kwargs["input"]
        assert "Who pays return shipping?" in kwargs["input"]

        return SimpleNamespace(
            output_text="Northstar provides a prepaid label [returns.md]."
        )

    fake_client = SimpleNamespace(
        responses=SimpleNamespace(create=fake_create)
    )

    monkeypatch.setattr(
        "app.ai_service.retrieve_policies",
        fake_retrieve_policies,
    )
    monkeypatch.setattr("app.ai_service.client", fake_client)

    reply = generate_reply("Who pays return shipping?")

    assert reply == "Northstar provides a prepaid label [returns.md]."