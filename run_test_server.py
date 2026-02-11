#!/usr/bin/env python3
"""
Simple test server to verify the backend works
"""
import os
import sys
import threading
import time

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment variables for testing
os.environ['COHERE_API_KEY'] = 'dummy-test-key'
os.environ['QDRANT_URL'] = 'https://test-cluster.qdrant.tech:6333'
os.environ['QDRANT_API_KEY'] = 'dummy-test-key'

def start_server():
    try:
        from backend.minimal_api import app
        import uvicorn
        
        print("Starting server on http://localhost:8000")
        print("Environment variables set for testing")
        
        # Run the server
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()