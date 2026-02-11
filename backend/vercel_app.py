"""
Vercel Entry Point for FastAPI Application
This file serves as the main entry point for Vercel deployment.
It initializes the FastAPI app without requiring external service initialization at startup.
"""
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for querying the RAG knowledge base",
    version="1.0.0"
)

# Add basic routes that don't require external services
@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "api"}

@app.get("/status")
def status():
    # Check if environment variables are available
    has_cohere = bool(os.getenv("COHERE_API_KEY"))
    has_qdrant_url = bool(os.getenv("QDRANT_URL"))
    has_qdrant_key = bool(os.getenv("QDRANT_API_KEY"))

    return {
        "status": "operational",
        "environment_configured": has_cohere and has_qdrant_url and has_qdrant_key,
        "has_cohere": has_cohere,
        "has_qdrant_url": has_qdrant_url,
        "has_qdrant_key": has_qdrant_key
    }

# Define models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    collection_name: str = "book_knowledge_base"

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    total_chunks: int

# Placeholder for query endpoint - will be replaced when environment is ready
@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    # Check if required environment variables are available
    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        return QueryResponse(
            query=request.query,
            response=f"Service not configured. Missing environment variables: {missing_vars}. Please set all required environment variables in your deployment platform.",
            sources=[],
            total_chunks=0
        )

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
    except ImportError as e:
        return QueryResponse(
            query=request.query,
            response=f"Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment: {str(e)}",
            sources=[],
            total_chunks=0
        )

    # If environment is configured, import and delegate to the full implementation
    try:
        from api import query_endpoint as full_query_endpoint
        return full_query_endpoint(request)
    except ImportError as e:
        logger.error(f"Failed to import full query endpoint: {e}")
        return QueryResponse(
            query=request.query,
            response=f"Service temporarily unavailable: {str(e)}",
            sources=[],
            total_chunks=0
        )

# Placeholder for ask endpoint
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str

@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    # Check if required environment variables are available
    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        return AskResponse(
            question=request.question,
            answer=f"Service not configured. Missing environment variables: {missing_vars}. Please set all required environment variables in your deployment platform."
        )

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
    except ImportError as e:
        return AskResponse(
            question=request.question,
            answer=f"Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment: {str(e)}"
        )

    # If environment is configured, import and delegate to the full implementation
    try:
        from api import ask_endpoint as full_ask_endpoint
        return full_ask_endpoint(request)
    except ImportError as e:
        logger.error(f"Failed to import full ask endpoint: {e}")
        return AskResponse(
            question=request.question,
            answer=f"Service temporarily unavailable: {str(e)}"
        )

# This is the entry point that Vercel will look for
application = app  # Alternative name for Vercel

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))