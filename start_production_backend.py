#!/usr/bin/env python3
"""
Production-ready backend server with environment variables
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path)

def start_production_server():
    # Verify environment variables are loaded
    required_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {missing_vars}")
        print("Please set all required environment variables in your .env file")
        sys.exit(1)
    
    print("Environment variables loaded successfully")
    print(f"Cohere API key length: {len(os.getenv('COHERE_API_KEY', ''))}")
    print(f"Qdrant URL: {os.getenv('QDRANT_URL', '')[:50]}...")
    
    try:
        # Import and start the server
        from backend.api import app
        import uvicorn
        
        port = int(os.getenv('PORT', 8000))
        host = os.getenv('HOST', '0.0.0.0')
        
        print(f"Starting server on {host}:{port}")
        print("Server is ready to accept connections...")
        
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level=os.getenv('LOG_LEVEL', 'info')
        )
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_production_server()