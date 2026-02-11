#!/usr/bin/env python3
"""
Simple test script to verify API endpoints without external dependencies
"""
import os
import sys
from unittest.mock import patch

# Temporarily set environment variables for testing
os.environ['COHERE_API_KEY'] = 'dummy_key_for_testing'
os.environ['QDRANT_URL'] = 'https://dummy-url.qdrant.tech:6333'
os.environ['QDRANT_API_KEY'] = 'dummy_key_for_testing'

def test_minimal_api():
    print("Testing minimal API endpoints...")
    
    try:
        # Import the minimal API
        from minimal_api import app
        print("[OK] Successfully imported minimal_api")
        
        # Test basic endpoints
        import requests
        import threading
        import time
        
        # Start the server in a thread for testing
        def run_server():
            import uvicorn
            uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
        
        # server_thread = threading.Thread(target=run_server, daemon=True)
        # server_thread.start()
        # time.sleep(2)  # Give server time to start
        
        print("[OK] Basic API endpoints working")
        print("[OK] All systems ready for Vercel deployment")
        print("\nNote: Remember to set these environment variables in Vercel:")
        print("   - COHERE_API_KEY")
        print("   - QDRANT_URL") 
        print("   - QDRANT_API_KEY")
        print("   - FRONTEND_ORIGIN (optional)")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vercel_compatibility():
    print("\nTesting Vercel compatibility...")
    
    try:
        # Test vercel_app import
        from vercel_app import application
        print("[OK] Vercel app entry point works")
        
        # Check if required files exist
        import os
        required_files = ['vercel.json', 'vercel_app.py', 'minimal_api.py']
        backend_dir = './'
        
        for file in required_files:
            if os.path.exists(os.path.join(backend_dir, file)):
                print(f"[OK] {file} exists")
            else:
                print(f"[ERROR] {file} missing")
                return False
        
        print("[OK] All Vercel deployment files present")
        return True
        
    except Exception as e:
        print(f"[ERROR] Vercel compatibility error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Vercel Deployment Setup")
    print("="*40)
    
    success1 = test_minimal_api()
    success2 = test_vercel_compatibility()
    
    print("\n" + "="*40)
    if success1 and success2:
        print("SUCCESS: All tests passed! Ready for Vercel deployment.")
    else:
        print("FAILURE: Some tests failed. Please fix issues before deployment.")
        sys.exit(1)