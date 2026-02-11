#!/usr/bin/env python3
"""
Backend server startup with proper environment loading
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from the backend .env file
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

# Add backend directory to Python path
sys.path.insert(0, backend_dir)

def start_server():
    print("Loading environment variables...")
    
    # Check if environment variables are properly loaded
    cohere_key = os.getenv('COHERE_API_KEY')
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    
    if not cohere_key or not qdrant_url or not qdrant_key:
        print("ERROR: Required environment variables are not set properly!")
        print(f"COHERE_API_KEY set: {'Yes' if cohere_key else 'No'}")
        print(f"QDRANT_URL set: {'Yes' if qdrant_url else 'No'}")
        print(f"QDRANT_API_KEY set: {'Yes' if qdrant_key else 'No'}")
        return
    
    print("Environment variables loaded successfully!")
    print(f"Cohere key preview: {cohere_key[:10]}...")
    print(f"Qdrant URL: {qdrant_url}")
    
    try:
        # Import the main API
        print("Importing backend API...")
        from api import app  # Import from backend directory
        print("API imported successfully!")
        
        # Test the connection to Cohere and Qdrant
        print("Testing API connections...")
        import cohere
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
        import urllib.parse
        
        # Initialize Cohere client
        co = cohere.Client(cohere_key)
        print("✅ Cohere client initialized")
        
        # Parse the URL to extract host properly
        parsed_url = urllib.parse.urlparse(qdrant_url)
        host = parsed_url.hostname if parsed_url.hostname else qdrant_url.replace("https://", "").replace(":6333", "").split('/')[0]
        
        # Initialize Qdrant client
        client = QdrantClient(
            host=host,
            api_key=qdrant_key,
            port=6333 if parsed_url.port else 6333,
            https=True
        )
        print("✅ Qdrant client initialized")
        
        # Test connection to Qdrant
        try:
            collections = client.get_collections().collections
            print(f"✅ Connected to Qdrant. Available collections: {[col.name for col in collections]}")
        except Exception as e:
            print(f"⚠️  Could not connect to Qdrant (this is OK if collection doesn't exist yet): {e}")
        
        # Start the server
        import uvicorn
        port = int(os.getenv('PORT', 8000))
        
        print(f"🚀 Starting server on port {port}...")
        print("The server is ready to accept connections!")
        
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed in the backend directory")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(backend_dir, "requirements.txt")])
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()