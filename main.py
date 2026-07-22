from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

from rag_engine import ingest_pdf, ask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("data", exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    num_chunks = ingest_pdf(path, doc_id=file.filename)
    return {"filename": file.filename, "chunks_added": num_chunks}

@app.post("/chat")
async def chat(question: str = Form(...)):
    answer, sources = ask(question)
    return {"answer": answer, "sources": sources}

app.mount("/", StaticFiles(directory="static", html=True), name="static")