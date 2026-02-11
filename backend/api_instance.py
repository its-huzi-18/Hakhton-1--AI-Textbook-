"""
API Instance for Vercel Deployment
This file creates the FastAPI app instance for Vercel to import.
"""
from api import app

# Export the app for Vercel
app_instance = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)