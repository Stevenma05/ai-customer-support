from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4-mini",
    input="Reply with exactly: ResolveAI connection successful",
    max_output_tokens=100
)

print(response.output_text)