import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY, GEMINI_EMBED_MODEL

def get_embeddings_model(task_type: str = "retrieval_query") -> GoogleGenerativeAIEmbeddings:
    """
    Initializes and returns the Google Gemini embeddings wrapper.
    Ensures that the API key is passed and the correct task type is set for retrieval.
    task_type:
        "retrieval_query"    -- User query at inference
        "retrieval_document" -- Chunking phase for vector db
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

    # High-quality embeddings model mapped for retrieval query tasks
    embeddings = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBED_MODEL,
        google_api_key=GOOGLE_API_KEY,
        task_type=task_type,
    )
    
    return embeddings
