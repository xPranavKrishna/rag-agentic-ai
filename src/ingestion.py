import os
import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_INDEX_NAME,
    PINECONE_REGION,
    check_keys,
)


def create_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    existing_indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION,
            ),
        )
        print(f"Created Pinecone index: {PINECONE_INDEX_NAME}")

    return pc


def run_ingestion(pdf_path: str):
    check_keys()

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}\n"
            "Put Ebook-Agentic-AI.pdf inside the data folder."
        )

    print("Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    print(f"Loaded {len(pages)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)

    # Keep the page number in metadata so retrieved chunks can be traced back.
    for chunk in chunks:
        page_number = chunk.metadata.get("page", 0) + 1
        chunk.metadata["page_number"] = page_number
        chunk.metadata["source"] = Path(pdf_path).name

    print(f"Created {len(chunks)} chunks")

    create_index()

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "data/Ebook-Agentic-AI.pdf"
    run_ingestion(pdf)
