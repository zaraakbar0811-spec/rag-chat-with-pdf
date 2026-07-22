# 📄 Chat with your PDF — RAG App

A Retrieval-Augmented Generation (RAG) application that lets you upload a PDF and ask questions about its content. Built end-to-end with a Python backend, local embeddings, a vector database, and a free hosted LLM — no paid APIs required.

## How it works

```
PDF Upload → Text Extraction → Chunking → Embedding → Vector Store (ChromaDB)
                                                              ↓
User Question → Embed Question → Similarity Search → Retrieve Top Chunks
                                                              ↓
                              Chunks + Question → LLM (Groq/Llama 3.1) → Answer
```

The app retrieves only the most relevant pieces of the uploaded document and feeds them to the LLM as context, so answers are grounded in the actual PDF content instead of the model's general training data.

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Backend | FastAPI | Lightweight, async, easy to extend |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Runs locally, no API cost |
| Vector store | ChromaDB | Simple persistence, pure Python |
| LLM | Groq (Llama 3.1 8B) | Free tier, fast inference |
| Frontend | HTML + vanilla JS | No build step, easy to read |

## Features

- Upload any PDF and have it automatically chunked and indexed
- Ask natural-language questions and get answers grounded in the document
- Re-uploading the same file replaces its old chunks instead of duplicating them
- Fully free to run — local embeddings + Groq's free API tier

## Demo

![Chat with your PDF demo](screenshots/chat-demo.png)

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/zaraakbar0811-spec/rag-chat-with-pdf.git
cd rag-chat-with-pdf
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate it
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (no credit card required)
3. Create an API key under **API Keys**

### 5. Set up your environment file

Copy the example file and add your key:

```bash
cp .env.example .env
```

Then open `.env` and paste in your key:

```
GROQ_API_KEY=your_actual_key_here
```

### 6. Run the app

```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

### 7. Try it out

Upload the included sample PDF (`data/cybersecurity_certifications.pdf`) and ask:

- "What is OSCP?"
- "Which certification is best for someone with no security experience?"
- "Compare OSCP and CEH — which is more hands-on?"

## Project Structure

```
rag-chat-with-pdf/
├── data/                # Uploaded PDFs (sample included)
├── static/
│   └── index.html       # Frontend chat UI
├── main.py              # FastAPI routes
├── rag_engine.py         # Chunking, embedding, retrieval, generation logic
├── requirements.txt
├── .env.example          # Template for required environment variables
└── .gitignore
```

## Limitations / Future Improvements

- Single-document context per session (no multi-file cross-referencing yet)
- No conversation memory — each question is treated independently
- No source citation shown in the UI yet (chunks are retrieved but not displayed)
- Chunking is word-count based rather than semantic/sentence-aware

## License

MIT
