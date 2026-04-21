"""
rag/retrieval.py
================
Owns two responsibilities:
  1. Query-time: vectorstore connection + retriever factory (used by agent tools)
  2. Ingest-time: upload function (called by ingest.py after chunking)
"""

from typing import List, Optional

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from config import (
    GOOGLE_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
    GEMINI_EMBED_MODEL,
    TOP_K_RETRIEVAL,
)


# ── Shared embeddings factory ─────────────────────────────────────────────────

def get_embeddings(task_type: str = "retrieval_query") -> GoogleGenerativeAIEmbeddings:
    """
    Returns a Gemini embeddings model.

    task_type:
      "retrieval_query"    — used at query time (agent tools)
      "retrieval_document" — used at ingest time (upsert)
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing from environment.")
    return GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBED_MODEL,
        google_api_key=GOOGLE_API_KEY,
        task_type=task_type,
    )


# ── Query-time helpers ────────────────────────────────────────────────────────

def get_vectorstore() -> PineconeVectorStore:
    """Opens a read connection to the existing Pinecone index."""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is missing. Add it to .env")
    return PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=get_embeddings(task_type="retrieval_query"),
        pinecone_api_key=PINECONE_API_KEY,
        namespace=PINECONE_NAMESPACE or None,
    )


def get_retriever(role_filter: Optional[str] = None):
    """
    Returns a configured retriever with optional ACL filter.

    The Pinecone filter restricts results to categories the role
    is allowed to access:
        {"category": {"$in": ["kb", "policies"]}}
    """
    from guardrails.acl import get_allowed_departments_for_role

    search_kwargs: dict = {"k": TOP_K_RETRIEVAL}

    if role_filter:
        allowed = get_allowed_departments_for_role(role_filter)
        if allowed:
            search_kwargs["filter"] = {"category": {"$in": allowed}}

    return get_vectorstore().as_retriever(search_kwargs=search_kwargs)


# ── Ingest-time helper ────────────────────────────────────────────────────────

def upload_to_pinecone(chunks: List[Document]) -> None:
    """
    Batch-upserts all chunks into Pinecone.
    Called only by ingest.py — not used at query time.
    """
    if not chunks:
        print("⚠️   No chunks to upload — skipping.")
        return

    print(f"\n🚀  Upserting {len(chunks)} chunks → '{PINECONE_INDEX_NAME}'…")
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=get_embeddings(task_type="retrieval_document"),
        index_name=PINECONE_INDEX_NAME,
        pinecone_api_key=PINECONE_API_KEY,
        namespace=PINECONE_NAMESPACE or None,
    )
    print("✅  Upsert complete.\n")
