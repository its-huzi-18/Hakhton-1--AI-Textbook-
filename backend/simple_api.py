"""
Simple Vercel-compatible FastAPI app that handles dependencies gracefully
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(
    title="RAG Chatbot API - Simple Version",
    description="Simple API for Vercel deployment with graceful dependency handling",
    version="1.0.0"
)

# Add CORS middleware
frontend_origin = os.getenv("FRONTEND_ORIGIN", "https://hakhton-ai-textbook.vercel.app")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "https://hakhton-ai-textbook.vercel.app", "http://localhost:3000", "http://localhost:3001"],
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

    # Check if dependencies can be imported
    deps_available = True
    try:
        import cohere
        import qdrant_client
    except ImportError:
        deps_available = False

    return {
        "status": "operational",
        "environment_configured": has_cohere and has_qdrant_url and has_qdrant_key,
        "dependencies_available": deps_available,
        "has_cohere": has_cohere,
        "has_qdrant_url": has_qdrant_url,
        "has_qdrant_key": has_qdrant_key
    }

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    answer: str

@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    # Check if environment variables are set
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

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
    except ImportError as e:
        return AskResponse(
            question=request.question,
            answer=f"Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment. Error: {str(e)}"
        )

    # If we get here, dependencies are available, but we might not have the full API
    # Return a message indicating that the service is ready but needs to be initialized
    return AskResponse(
        question=request.question,
        answer="System initialized but knowledge base not accessible. The backend is properly configured with dependencies and environment variables."
    )

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    collection_name: str = "book_knowledge_base"

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    total_chunks: int

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    # Check if environment variables are set
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

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
    except ImportError as e:
        return QueryResponse(
            query=request.query,
            response=f"Dependencies not installed. Please ensure cohere and qdrant-client are available in your environment. Error: {str(e)}",
            sources=[],
            total_chunks=0
        )

    # If we get here, dependencies are available, but we might not have the full API
    # Return a message indicating that the service is ready but needs to be initialized
    return QueryResponse(
        query=request.query,
        response="System initialized but knowledge base not accessible. The backend is properly configured with dependencies and environment variables.",
        sources=[],
        total_chunks=0
    )

@app.get("/collections")
def get_collections():
    # Check if environment variables are set
    missing_vars = []
    if not os.getenv("COHERE_API_KEY"):
        missing_vars.append("COHERE_API_KEY")
    if not os.getenv("QDRANT_URL"):
        missing_vars.append("QDRANT_URL")
    if not os.getenv("QDRANT_API_KEY"):
        missing_vars.append("QDRANT_API_KEY")

    if missing_vars:
        return {"error": f"Service not configured. Missing environment variables: {missing_vars}"}

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
        from qdrant_client import QdrantClient
        
        # Try to connect to Qdrant
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        from urllib.parse import urlparse
        parsed_url = urlparse(qdrant_url)
        host = parsed_url.hostname if parsed_url.hostname else qdrant_url.replace("https://", "").replace(":6333", "").split('/')[0]

        client = QdrantClient(
            host=host,
            api_key=qdrant_api_key,
            port=6333 if parsed_url.port else 6333,
            https=True
        )
        
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        return {"collections": collection_names}
    except ImportError as e:
        return {"error": f"Dependencies not installed: {str(e)}"}
    except Exception as e:
        return {"error": f"Error connecting to Qdrant: {str(e)}"}

@app.post("/initialize-knowledge-base")
def initialize_knowledge_base():
    """Endpoint to initialize the knowledge base by processing the book content"""
    # Check if environment variables are set
    missing_vars = []
    if not os.getenv("COHERE_API_KEY"):
        missing_vars.append("COHERE_API_KEY")
    if not os.getenv("QDRANT_URL"):
        missing_vars.append("QDRANT_URL")
    if not os.getenv("QDRANT_API_KEY"):
        missing_vars.append("QDRANT_API_KEY")
    if not os.getenv("TARGET_URL"):
        missing_vars.append("TARGET_URL")

    if missing_vars:
        return {"error": f"Missing environment variables: {missing_vars}"}

    # Check if dependencies are available
    try:
        import cohere
        import qdrant_client
    except ImportError as e:
        return {"error": f"Dependencies not installed: {str(e)}"}

    try:
        # Import and run the process_book function
        from process_book import process_book
        import threading
        
        # Run the process_book function in a separate thread to avoid timeout
        def run_process():
            try:
                process_book()
                print("Knowledge base initialization completed successfully!")
            except Exception as e:
                print(f"Error during knowledge base initialization: {str(e)}")
        
        thread = threading.Thread(target=run_process)
        thread.daemon = True
        thread.start()
        
        return {"message": "Knowledge base initialization started. This may take several minutes depending on your content size."}
    except Exception as e:
        return {"error": f"Error initializing knowledge base: {str(e)}"}

# This is the entry point that Vercel will use
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))