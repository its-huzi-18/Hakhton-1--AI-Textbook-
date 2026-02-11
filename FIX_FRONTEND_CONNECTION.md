# Fixing Frontend-Backend Connection Issue

## Problem
The deployed frontend at `https://hakhton-ai-textbook.vercel.app` is trying to connect to `http://localhost:8000/ask`, causing a CORS error because:
1. The frontend is on `https://hakhton-ai-textbook.vercel.app` (deployed site)
2. It's trying to connect to `http://localhost:8000` (local backend that doesn't exist from deployed site)
3. This creates a cross-origin request that fails

## Solution
You need to set the environment variables during the frontend build process.

### Step 1: Identify Your Backend URL
From your .env file, your backend is deployed at:
`BACKEND_ORIGIN="https://hakhton-1-ai-textbook-backend.vercel.app/"`

### Step 2: Set Environment Variables for Frontend Deployment
During the Docusaurus site deployment (on Vercel), set these environment variables:

```
RAG_CHATBOT_API_URL=https://hakhton-1-ai-textbook-backend.vercel.app/
NEXT_PUBLIC_RAG_CHATBOT_API_URL=https://hakhton-1-ai-textbook-backend.vercel.app/
```

### Step 3: How to Set Environment Variables on Vercel
1. Go to your Vercel dashboard
2. Select your frontend project (`hakhton-ai-textbook`)
3. Go to Settings → Environment Variables
4. Add the following variables:
   - Key: `RAG_CHATBOT_API_URL`, Value: `https://hakhton-1-ai-textbook-backend.vercel.app/`
   - Key: `NEXT_PUBLIC_RAG_CHATBOT_API_URL`, Value: `https://hakhton-1-ai-textbook-backend.vercel.app/`
5. Redeploy your project

### Step 4: Verify Backend is Accessible
Make sure your backend at `https://hakhton-1-ai-textbook-backend.vercel.app/` is running and accessible:
- Visit: `https://hakhton-1-ai-textbook-backend.vercel.app/health`
- Should return a healthy status

### Step 5: Verify CORS Configuration
Your backend should have `FRONTEND_ORIGIN="https://hakhton-ai-textbook.vercel.app/"` in its environment variables to allow requests from your frontend.

## Testing
After redeployment with the correct environment variables:
1. Open your deployed site
2. Open browser developer tools
3. Try asking a question in the chatbot
4. The network tab should show requests going to `https://hakhton-1-ai-textbook-backend.vercel.app/ask` instead of `http://localhost:8000/ask`