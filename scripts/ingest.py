from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os
from pinecone import Pinecone

load_dotenv()

""""
Path(__file__).resolve().parent finds the folder containing ingest.py.
/ "knowledge_base" builds the path to your policy folder.
"""
knowledge_base = Path(__file__).resolve().parent.parent / "knowledge_base"

# Split into chunks of 700 characters with 100 characters overlapping
splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
)

all_chunks = []

# .glob("*.md") finds Markdown files; sorted(...) gives them a consistent order.
for file_path in sorted(knowledge_base.glob("*.md")):
    text = file_path.read_text(encoding="utf-8")
    
    # Creating the documents containing the test and source for each chunk
    chunks = splitter.create_documents(
        [text],
        metadatas=[{"source": file_path.name}],
    )
    
    # Gather chunks from all three files into one list
    all_chunks.extend(chunks)
    
    print(f"Source: {file_path.name}")
    print(f"Character: {len(text)}")
    
if not all_chunks:
    raise ValueError("No policy chunks found!")
    
# selects an embedding model, separate from your chat model.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# extracts their text
texts = [chunk.page_content for chunk in all_chunks]
# sends the text to OpenAI and returns vectors (usually 1536) in the same order.
vectors = embeddings.embed_documents(texts)

print(f"\nCreated {len(vectors)} embeddings")
print(f"Numbers per embedding: {len(vectors[0])}")
print(f"First five numbers: {vectors[0][:5]}")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("resolveai-support")

records = []

for number, (chunk, vector) in enumerate(zip(all_chunks, vectors, strict=True)):
    records.append({
        "id": f"chunk-{number}",
        "values": vector,
        "metadata": {
            "text": chunk.page_content,
            "source": chunk.metadata["source"],
        },
    })
    
result = index.upsert(
    vectors=records,
    namespace="northstar-v1"
)

print(f"Uploaded {result.upserted_count} records")