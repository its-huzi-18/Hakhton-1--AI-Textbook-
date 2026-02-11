# Test script to verify backend connectivity and status
import requests
import json

BACKEND_URL = "https://hakhton-1-ai-textbook-backend.vercel.app"  # Replace with your actual backend URL

def test_backend():
    print("Testing backend connectivity...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print(f"Root endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Not OK'}")
    except Exception as e:
        print(f"Root endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        print(f"Health endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Not OK'}")
    except Exception as e:
        print(f"Health endpoint error: {e}")
    
    # Test collections endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/collections")
        print(f"Collections endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Not OK'}")
    except Exception as e:
        print(f"Collections endpoint error: {e}")

    # Test ask endpoint with a sample request
    try:
        sample_data = {"question": "What is this book about?"}
        response = requests.post(f"{BACKEND_URL}/ask", json=sample_data)
        print(f"Ask endpoint: {response.status_code} - {response.json() if response.status_code == 200 else 'Not OK or Error'}")
    except Exception as e:
        print(f"Ask endpoint error: {e}")

if __name__ == "__main__":
    test_backend()