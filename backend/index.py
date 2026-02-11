"""
Index entry point for Vercel deployment
"""
from api import app

# Vercel expects the FastAPI app to be available at the module level
app_instance = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)