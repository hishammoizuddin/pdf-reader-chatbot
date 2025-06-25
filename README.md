# 📄 PDF Reader Chatbot

An **AI-powered** web application that allows users to upload PDF documents and ask natural language questions. The app retrieves the most relevant content from the uploaded PDFs and generates context-aware responses using OpenAI’s GPT models.

---

## 🚀 Watch the Demo

[![Watch the demo](https://img.youtube.com/vi/2i93_Bn4xKE/0.jpg)](https://www.youtube.com/watch?v=2i93_Bn4xKE)

---

## 🧠 How It Works

1. **PDF Upload**  
   - Users upload one or more PDF files through the React.js frontend.
   - The backend extracts raw text using `pdfplumber` and chunks it with token overlap for better context preservation.

2. **Embedding + Storage**  
   - Each chunk is converted into a dense vector using a `sentence-transformers` model.
   - The vectors are stored in a **Pinecone** vector database for fast semantic retrieval.

3. **Semantic Search + GPT Answering**  
   - When a user submits a question, it is embedded and used to retrieve top-k most similar chunks from Pinecone.
   - These chunks are passed as knowledge context to the **OpenAI GPT API**, which generates an accurate and grounded answer.

---

## 🛠 Tech Stack

### 🔧 Backend
- **Python**, **FastAPI**
- `pdfplumber`, `sentence-transformers`, `pinecone-client`, `openai`
- Embedding model: `all-MiniLM-L6-v2` (or similar)
- Stores vectors in Pinecone, retrieves top-K matches, calls GPT for response

### 💻 Frontend
- **React.js**, **Axios**
- Multi-file PDF upload
- Chat-style interface with dynamic user/bot messages
- In-session history viewer and message scrollback

---

## 📂 Project Structure

```
/backend
  ├── main.py           # FastAPI endpoints
  ├── pdf_utils.py      # PDF parsing and chunking logic
  ├── search.py         # Pinecone-based semantic search
  └── requirements.txt

/frontend
  ├── App.js            # Main React component
  ├── App.css           # Dark-themed styling
  ├── index.js, index.css
```

---

## ⚡️ Features

- ✅ Upload and process multiple PDFs
- ✅ Natural language Q&A over user-provided content
- ✅ Real-time chat experience with loading indicators
- ✅ Local chat history by session
- ✅ Dark theme interface with intuitive UX

---

## 📦 Setup & Run

### 1. Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm start
```

> Make sure to replace `localhost:8000` URLs with your deployed backend address if needed.

---

## 🧪 Future Improvements
- Add persistent user accounts and cloud-based chat history
- Support for displaying source (file name, page number) with answers
- Deploy to Vercel (Frontend) + Render/Fly.io (Backend)

---

## 📬 Contact

Made by [Mohammed Hisham Moizuddin](https://github.com/hishammoizuddin)  
Open to feedback, collaboration, and cool ideas!
