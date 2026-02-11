"""
Minimal Vercel-compatible FastAPI app
This version avoids all external dependencies during build time
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import importlib.util

app = FastAPI(
    title="RAG Chatbot API - Minimal Version",
    description="Minimal API for Vercel deployment",
    version="1.0.0"
)

# Add CORS middleware - this is crucial for frontend integration
frontend_origin = os.getenv("FRONTEND_ORIGIN", "https://hakhton-ai-textbook.vercel.app")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "https://hakhton-ai-textbook.vercel.app", "http://localhost:3000", "http://localhost:3001"],  # Allow your frontend origin and localhost for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running on Vercel!", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy", "environment": "vercel"}

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

# Dynamic import of full API when environment is ready
def get_full_api():
    """Dynamically import the full API when dependencies are available"""
    if os.getenv("COHERE_API_KEY") and os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY"):
        try:
            # Check if we can import the required packages
            import cohere
            import qdrant_client
            from api import app as full_app
            return full_app
        except ImportError as e:
            print(f"Could not import full API: {e}")
            return None
    return None

# Conditional endpoints - only add if environment is properly configured
full_api = get_full_api()

if full_api:
    # If full API is available, we can add the query and ask endpoints
    # We'll add them directly to this app
    from pydantic import BaseModel
    from typing import List, Dict, Any
    
    class QueryRequest(BaseModel):
        query: str
        top_k: int = 5
        collection_name: str = "book_knowledge_base"

    class QueryResponse(BaseModel):
        query: str
        response: str
        sources: List[Dict[str, Any]]
        total_chunks: int

    class AskRequest(BaseModel):
        question: str

    class AskResponse(BaseModel):
        question: str
        answer: str

    @app.post("/query", response_model=QueryResponse)
    def query_endpoint(request: QueryRequest):
        # Dynamically import the full implementation when called
        try:
            from api import query_endpoint as full_query_endpoint
            return full_query_endpoint(request)
        except ImportError as e:
            raise HTTPException(status_code=500, detail=f"Service temporarily unavailable: {str(e)}")

    @app.post("/ask", response_model=AskResponse)
    def ask_endpoint(request: AskRequest):
        # Dynamically import the full implementation when called
        try:
            from api import ask_endpoint as full_ask_endpoint
            return full_ask_endpoint(request)
        except ImportError as e:
            raise HTTPException(status_code=500, detail=f"Service temporarily unavailable: {str(e)}")

    @app.get("/collections")
    def get_collections():
        try:
            from api import get_collections as full_get_collections
            return full_get_collections()
        except ImportError as e:
            raise HTTPException(status_code=500, detail=f"Service temporarily unavailable: {str(e)}")

else:
    # If full API is not available, provide informative endpoints
    from pydantic import BaseModel
    from typing import List, Dict, Any
    
    class QueryRequest(BaseModel):
        query: str
        top_k: int = 5
        collection_name: str = "book_knowledge_base"

    class QueryResponse(BaseModel):
        query: str
        response: str
        sources: List[Dict[str, Any]]
        total_chunks: int

    class AskRequest(BaseModel):
        question: str

    class AskResponse(BaseModel):
        question: str
        answer: str

    @app.post("/query", response_model=QueryResponse)
    def query_endpoint(request: QueryRequest):
        missing_vars = []
        if not os.getenv("COHERE_API_KEY"):
            missing_vars.append("COHERE_API_KEY")
        if not os.getenv("QDRANT_URL"):
            missing_vars.append("QDRANT_URL")
        if not os.getenv("QDRANT_API_KEY"):
            missing_vars.append("QDRANT_API_KEY")
        
        if missing_vars:
            return QueryResponse(
                query=request.query,
                response=f"Service not configured. Missing environment variables: {missing_vars}. Please set all required environment variables in your deployment platform.",
                sources=[],
                total_chunks=0
            )
        
        return QueryResponse(
            query=request.query,
            response="Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment.",
            sources=[],
            total_chunks=0
        )

    @app.post("/ask", response_model=AskResponse)
    def ask_endpoint(request: AskRequest):
        missing_vars = []
        if not os.getenv("COHERE_API_KEY"):
            missing_vars.append("COHERE_API_KEY")
        if not os.getenv("QDRANT_URL"):
            missing_vars.append("QDRANT_URL")
        if not os.getenv("QDRANT_API_KEY"):
            missing_vars.append("QDRANT_API_KEY")
        
        if missing_vars:
            return AskResponse(
                question=request.question,
                answer=f"Service not configured. Missing environment variables: {missing_vars}. Please set all required environment variables in your deployment platform."
            )
        
        return AskResponse(
            question=request.question,
            answer="Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment."
        )

# This is the entry point that Vercel will use
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))