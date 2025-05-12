from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pinecone
import os
import uuid
import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create index
if "pdf-chatbot" not in pc.list_indexes().names():
    pc.create_index(
        name="pdf-chatbot",
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index("pdf-chatbot")

# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("all-mpnet-base-v2")

text_chunks = []
embeddings = []

def chunk_text(text, size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

# def process_text(text):
#     global text_chunks, embeddings
#     text_chunks = chunk_text(text)
#     embeddings = model.encode(text_chunks)

def process_text(text):
    global text_chunks
    text_chunks = chunk_text(text)
    embeddings = model.encode(text_chunks)

    vectors = [
        (str(uuid.uuid4()), emb.tolist(), {"text": chunk})
        for emb, chunk in zip(embeddings, text_chunks)
    ]
    index.upsert(vectors)

# def get_top_k_chunks(query, k=3):
#     query_vec = model.encode([query])
#     sims = cosine_similarity(query_vec, embeddings)[0]
#     top_k = np.argsort(sims)[-k:][::-1]
#     return [text_chunks[i] for i in top_k]

def get_top_k_chunks(query, k=7):
    query_vec = model.encode([query])[0].tolist()
    results = index.query(vector=query_vec, top_k=k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

