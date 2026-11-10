import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

load_dotenv()

def retrieve_policies(question: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("resolveai-support")

    question_vector = embeddings.embed_query(question)

    results = index.query(
        vector=question_vector,
        namespace="northstar-v1",
        top_k=5,
        include_metadata=True
    )

    return results.matches

if __name__ == "__main__":
    question = "Who pays shipping if I return a defective product?"
    matches = retrieve_policies(question)

    for match in matches:
        print(f"\nSource: {match.metadata['source']}")
        print(f"Score: {match.score:.3f}")
        print(match.metadata["text"])
        print("-" * 40)