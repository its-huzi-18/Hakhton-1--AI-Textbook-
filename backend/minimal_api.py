"""
Minimal Vercel-compatible FastAPI app
This version avoids all external dependencies during build time
"""
from fastapi import FastAPI
import os

app = FastAPI(
    title="RAG Chatbot API - Minimal Version",
    description="Minimal API for Vercel deployment",
    version="1.0.0"
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
    has_cohere = "COHERE_API_KEY" in os.environ
    has_qdrant = "QDRANT_URL" in os.environ
    
    return {
        "status": "operational",
        "environment_configured": has_cohere and has_qdrant,
        "has_cohere": has_cohere,
        "has_qdrant": has_qdrant
    }

# This is the entry point that Vercel will use
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))