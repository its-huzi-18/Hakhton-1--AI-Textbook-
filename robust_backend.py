#!/usr/bin/env python3
"""
Robust backend server startup that handles Qdrant connection gracefully
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
        
        # Temporarily override the environment variables in the current process
        original_environ = dict(os.environ)
        os.environ['COHERE_API_KEY'] = cohere_key
        os.environ['QDRANT_URL'] = qdrant_url
        os.environ['QDRANT_API_KEY'] = qdrant_key
        
        from api import app  # Import from backend directory
        print("✅ API imported successfully!")
        
        # Restore original environment if needed
        os.environ.clear()
        os.environ.update(original_environ)
        
        # Start the server
        import uvicorn
        port = int(os.getenv('PORT', 8000))
        
        print(f"🚀 Starting server on port {port}...")
        print("💡 The server is ready to accept connections!")
        print("📋 Available endpoints: /, /health, /ask, /query, /collections")
        print("📝 Note: Some endpoints may show errors if knowledge base is not populated yet")
        
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