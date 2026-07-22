import os
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# --- Setup ---
client = chromadb.PersistentClient(path="chroma_db")

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"   # small, fast, free, local
)

collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embed_fn
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# --- 1. Load + chunk PDF ---
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text, chunk_size=300, overlap=30):   # was 500/50
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


# --- 2. Ingest a PDF into the vector store ---
def ingest_pdf(path, doc_id):
       # Remove old chunks for this doc if they exist (avoids duplicates on re-upload)
       existing = collection.get(where={"doc_id": doc_id})
       if existing and existing["ids"]:
           collection.delete(ids=existing["ids"])

       text = extract_text_from_pdf(path)
       chunks = chunk_text(text)
       ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
       metadatas = [{"doc_id": doc_id} for _ in chunks]
       collection.add(documents=chunks, ids=ids, metadatas=metadatas)
       return len(chunks)

# --- 3. Retrieve relevant chunks ---
def retrieve(query, top_k=2):   # was 4, try 2
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0]


# --- 4. Generate an answer using retrieved context ---
def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question using only the context below.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {query}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def ask(query):
    chunks = retrieve(query)
    answer = generate_answer(query, chunks)
    return answer, chunks