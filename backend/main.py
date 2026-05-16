from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import (
    extract_pdf_text,
    chunk_text,
    store_in_chromadb,
    retrieve_context,
    ask_mistral
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Question schema
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI College Chatbot Backend Running"
    }


# Upload PDF endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    text = extract_pdf_text(file.file)

    chunks = chunk_text(text)

    store_in_chromadb(chunks)

    return {
        "message": "PDF uploaded successfully",
        "chunks_stored": len(chunks)
    }


# Ask question endpoint
@app.post("/ask")
async def ask_question(data: QuestionRequest):

    context = retrieve_context(data.question)

    answer = ask_mistral(
        data.question,
        "\n".join(context)
    )

    return {
        "question": data.question,
        "answer": answer,
        "context": context
    }