"""
Simple test to verify that the FastAPI app can be imported correctly
"""
try:
    from api import app
    print("SUCCESS: Successfully imported FastAPI app from api.py")
    print(f"App title: {app.title}")
    print("Vercel should be able to recognize this FastAPI application")
except Exception as e:
    print(f"ERROR: Error importing app: {e}")
    exit(1)