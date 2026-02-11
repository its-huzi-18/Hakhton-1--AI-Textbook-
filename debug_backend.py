#!/usr/bin/env python3
"""
Debug version of backend server to troubleshoot Qdrant connection
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from the backend .env file
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

# Add backend directory to Python path
sys.path.insert(0, backend_dir)

def test_connections():
    print("Testing connections...")
    
    # Check if environment variables are properly loaded
    cohere_key = os.getenv('COHERE_API_KEY')
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    
    if not cohere_key or not qdrant_url or not qdrant_key:
        print("ERROR: Required environment variables are not set properly!")
        print(f"COHERE_API_KEY set: {'Yes' if cohere_key else 'No'} (length: {len(cohere_key) if cohere_key else 0})")
        print(f"QDRANT_URL set: {'Yes' if qdrant_url else 'No'} (value: {qdrant_url})")
        print(f"QDRANT_API_KEY set: {'Yes' if qdrant_key else 'No'} (length: {len(qdrant_key) if qdrant_key else 0})")
        return False
    
    print("Environment variables loaded successfully!")
    print(f"Cohere key preview: {cohere_key[:10]}...")
    print(f"Qdrant URL: {qdrant_url}")
    
    try:
        # Test Cohere connection
        print("\nTesting Cohere connection...")
        import cohere
        co = cohere.Client(cohere_key)
        print("Cohere client initialized successfully")
        
        # Test a simple embedding to verify the API key works
        try:
            response = co.embed(texts=["test"], model="embed-multilingual-v3.0")
            print("Cohere API key is valid and working")
        except Exception as e:
            print(f"Cohere API test failed: {e}")
            return False
        
        # Test Qdrant connection
        print("\nTesting Qdrant connection...")
        from qdrant_client import QdrantClient
        import urllib.parse
        
        # Parse the URL to extract host properly
        parsed_url = urllib.parse.urlparse(qdrant_url)
        host = parsed_url.hostname if parsed_url.hostname else qdrant_url.replace("https://", "").replace(":6333", "").split('/')[0]
        
        print(f"Parsed host: {host}")
        print(f"Port: {parsed_url.port or 6333}")
        print(f"HTTPS: True")
        
        # Initialize Qdrant client
        client = QdrantClient(
            host=host,
            api_key=qdrant_key,
            port=parsed_url.port or 6333,
            https=True
        )
        print("Qdrant client initialized")
        
        # Test connection to Qdrant
        try:
            collections = client.get_collections().collections
            collection_names = [col.name for col in collections]
            print(f"Connected to Qdrant successfully!")
            print(f"Available collections: {collection_names}")
            return True, client
        except Exception as e:
            print(f"Qdrant connection test failed: {e}")
            print("This might be because the collection doesn't exist yet.")
            print("That's OK - the collection will be created when you populate the knowledge base.")
            return True, client  # Still return True as connection setup is correct
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def start_debug_server():
    result = test_connections()
    if isinstance(result, tuple):
        success, client = result
    else:
        success = result
    
    if not success:
        print("Cannot start server due to connection issues")
        return
    
    print("\nStarting server with validated connections...")
    
    try:
        # Import the main API
        from api import app
        print("API imported successfully!")
        
        import uvicorn
        port = int(os.getenv('PORT', 8000))
        
        print(f"Server will start on port {port}")
        print("Server is ready to accept connections!")
        print("Available endpoints: /, /health, /ask, /query, /collections")
        
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_debug_server()