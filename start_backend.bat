@echo off
cd /d "D:\Vs Code-All-Things\Github Repo\Hakhton-1( AI Textbook)\backend"

set COHERE_API_KEY=dummy-test-key
set QDRANT_URL=https://test-cluster.qdrant.tech:6333
set QDRANT_API_KEY=dummy-test-key

echo Starting backend server...
python -m uvicorn minimal_api:app --host 0.0.0.0 --port 8000