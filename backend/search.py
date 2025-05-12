from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

text_chunks = []
embeddings = []

def chunk_text(text, size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

def process_text(text):
    global text_chunks, embeddings
    text_chunks = chunk_text(text)
    embeddings = model.encode(text_chunks)

def get_top_k_chunks(query, k=3):
    query_vec = model.encode([query])
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_k = np.argsort(sims)[-k:][::-1]
    return [text_chunks[i] for i in top_k]
