from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import requests

# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="college_docs"
)

# Extract PDF text
def extract_pdf_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# Split text into chunks
def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


# Store embeddings in ChromaDB
def store_in_chromadb(chunks):

    for idx, chunk in enumerate(chunks):

        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(idx)]
        )


# Retrieve relevant chunks
def retrieve_context(query, top_k=3):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


# Generate answer using Ollama Mistral
def ask_mistral(question, context):

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]