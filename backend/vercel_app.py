"""
Vercel Entry Point for FastAPI Application
This file serves as the main entry point for Vercel deployment.
It initializes the FastAPI app with proper error handling for environment variables.
"""
import os
import logging
from contextlib import suppress

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the FastAPI app with lazy initialization
def get_app():
    """Lazily initialize the FastAPI app to defer environment variable checks"""
    try:
        from fastapi import FastAPI
        
        # Initialize FastAPI app
        app = FastAPI(
            title="RAG Chatbot API",
            description="API for querying the RAG knowledge base",
            version="1.0.0"
        )
        
        # Add a simple route that doesn't require external services for basic functionality
        @app.get("/")
        def root():
            return {"message": "RAG Chatbot API is running", "status": "success"}
            
        @app.get("/health")
        def health():
            return {"status": "healthy", "service": "api"}
        
        # Conditionally add the full API routes if environment is properly configured
        required_env_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
        env_vars_present = all(var in os.environ for var in required_env_vars)
        
        if env_vars_present:
            logger.info("All required environment variables present, loading full API")
            # Import and add the full API routes
            try:
                # Dynamically import the rest of the API to avoid early initialization
                import importlib.util
                spec = importlib.util.spec_from_file_location("full_api", "api.py")
                full_api_module = importlib.util.module_from_spec(spec)
                
                # Add the app object to the module temporarily to avoid conflicts
                full_api_module.app = app
                
                # Execute the module to register routes, but skip the client initialization
                # by temporarily replacing the client initialization code
                spec.loader.exec_module(full_api_module)
                
            except Exception as e:
                logger.error(f"Error loading full API: {e}")
                # Add a fallback error route
                @app.get("/query")
                def query_error():
                    return {"error": "API not fully initialized due to configuration issues"}
        else:
            logger.warning(f"Missing required environment variables: {[var for var in required_env_vars if var not in os.environ]}")
            # Add a fallback route that explains the issue
            @app.post("/query")
            def query_error():
                return {"error": "API not configured - missing environment variables", 
                       "required": required_env_vars}
        
        return app
    except ImportError as e:
        logger.error(f"Error importing FastAPI: {e}")
        raise

# Create the app instance for Vercel
try:
    app = get_app()
except Exception as e:
    logger.error(f"Failed to create app: {e}")
    # Create a minimal app as fallback
    from fastapi import FastAPI
    app = FastAPI(title="RAG Chatbot API", description="API failed to initialize", version="1.0.0")
    
    @app.get("/")
    def error_root():
        return {"message": "API failed to initialize", "error": str(e)}

# This is the entry point that Vercel will look for
application = app  # Alternative name for Vercel

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))