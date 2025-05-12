from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pdf_utils import extract_text
from search import process_text, get_top_k_chunks
from typing import List
from fastapi import UploadFile
client = 'APIKEY' #CHANGE API KEY

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
    prompt = f"""Answer the question based only on the context below.

Context:
{chr(10).join(chunks)}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(chunks)
    return {"answer": response.choices[0].message.content}
