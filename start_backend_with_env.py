#!/usr/bin/env python3
"""
Script to start the backend server with proper environment variables for testing
"""
import os
import subprocess
import sys
import time

def start_server_with_env():
    # Set environment variables for testing (these are dummy values for testing only)
    env = os.environ.copy()
    env['COHERE_API_KEY'] = 'test-key-for-local-testing'
    env['QDRANT_URL'] = 'https://test-cluster.qdrant.tech:6333'
    env['QDRANT_API_KEY'] = 'test-key-for-local-testing'
    env['FRONTEND_ORIGIN'] = 'http://localhost:3000'
    
    print("Starting backend server with test environment variables...")
    print("Note: Real API keys are needed for actual functionality")
    
    # Start the server using the vercel-compatible app
    try:
        # Use the minimal_api.py which is designed for Vercel but works locally too
        process = subprocess.Popen([
            sys.executable, "-c", 
            """
import uvicorn
from backend.minimal_api import app
uvicorn.run(app, host='0.0.0.0', port=8000)
"""
        ], env=env, cwd=os.getcwd())
        
        print(f"Server started with PID: {process.pid}")
        print("Server should be available at http://localhost:8000")
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the server is responding
        try:
            import urllib.request
            import urllib.error
            
            try:
                response = urllib.request.urlopen('http://localhost:8000/', timeout=5)
                print("✅ Server is responding!")
                print(f"Status: {response.getcode()}")
                
                # Test the status endpoint
                status_response = urllib.request.urlopen('http://localhost:8000/status', timeout=5)
                import json
                status_data = json.loads(status_response.read().decode())
                print(f"Status: {status_data}")
                
            except urllib.error.URLError as e:
                print(f"❌ Server not responding: {e}")
                
        except ImportError:
            print("⚠️  Could not test server response (urllib not available)")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            process.terminate()
            
    except Exception as e:
        print(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server_with_env()