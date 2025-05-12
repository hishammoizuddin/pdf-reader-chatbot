from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pdf_utils import extract_text
from search import process_text, get_top_k_chunks
from typing import List
from fastapi import UploadFile
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload/")
async def upload(files: List[UploadFile] = File(...)):
    combined_text = ""
    for file in files:
        combined_text += extract_text(file.file) + "\n"
    process_text(combined_text)
    return {"message": f"{len(files)} PDFs processed"}

@app.post("/ask/")
async def ask(question: str = Form(...)):
    chunks = get_top_k_chunks(question)
    prompt = f"""
You are a helpful assistant that answers questions based on the context provided.

Use only the information in the context. Be specific, detailed, and use complete sentences.

Context:
{chr(10).join(chunks)}

Question: {question}
Answer:"""


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a precise, detailed assistant. Only use the context provided to answer the question thoroughly."},
            {"role": "user", "content": prompt}
        ]

    )
    return {"answer": response.choices[0].message.content}
