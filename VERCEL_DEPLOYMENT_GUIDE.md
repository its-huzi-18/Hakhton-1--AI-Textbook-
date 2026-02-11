# Vercel Deployment Guide for RAG Chatbot Backend

## Prerequisites

- Vercel account
- Access to Qdrant vector database (either cloud or self-hosted)
- Cohere API key
- The knowledge base must already be populated in your Qdrant instance

## Required Environment Variables

Set these environment variables in your Vercel project dashboard:

```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here (e.g., https://your-cluster-id.eu-central.aws.cloud.qdrant.io:6333)
QDRANT_API_KEY=your_qdrant_api_key_here
TARGET_URL=https://your-frontend-domain.vercel.app
```

## Step-by-Step Deployment Instructions

### 1. Prepare Your Vector Database

Before deploying the backend, you must populate your Qdrant vector database with the book content:

1. Deploy the backend temporarily to a local environment or Railway with the environment variables set
2. Run the `process_book.py` script to populate your Qdrant database:
   ```bash
   cd backend
   python process_book.py
   ```
3. Verify that the collection "book_knowledge_base" exists in your Qdrant instance

### 2. Deploy Backend to Vercel

1. Push your updated code (with the corrected requirements.txt) to your GitHub repository
2. Connect your repository to Vercel
3. During project setup, ensure the following:
   - Framework: Other (since it's a FastAPI app)
   - Root Directory: `/backend` (select this directory in Vercel)
   - Build Command: Leave blank (Vercel will detect automatically)
   - Output Directory: Leave blank
   - Install Command: `pip install -r minimal_requirements.txt` (or requirements.txt)

### 3. Configure Environment Variables in Vercel

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variables:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `TARGET_URL`: Your frontend URL

### 4. Redeploy

After setting the environment variables, redeploy your project from the Vercel dashboard.

### 5. Update Frontend Environment Variables

For your frontend (the Docusaurus site), set these environment variables in the Vercel dashboard for the frontend project:

```
RAG_CHATBOT_API_URL=https://your-backend-project-name.vercel.app
NEXT_PUBLIC_RAG_CHATBOT_API_URL=https://your-backend-project-name.vercel.app
```

## Troubleshooting

### Common Issues:

1. **"Service not configured. Missing environment variables"**: Check that all three environment variables are set in Vercel
2. **"Connection refused" or "Connection timeout"**: Verify your QDRant URL and API key are correct
3. **"No context chunks found for the query"**: The knowledge base hasn't been populated in Qdrant
4. **CORS errors**: The backend allows all origins, but check browser console for specific errors

### Verification Steps:

1. Visit your backend URL directly: `https://your-backend-project-name.vercel.app/`
   - Should return: `{"message": "RAG Chatbot API is running on Vercel!", "status": "success"}`
   
2. Check the status endpoint: `https://your-backend-project-name.vercel.app/status`
   - Should show: `"environment_configured": true`
   
3. Check the health endpoint: `https://your-backend-project-name.vercel.app/health`
   - Should return the list of collections if Qdrant connection is working

4. Test the /ask endpoint manually with a POST request to ensure it's working

## Important Notes

- The `minimal_api.py` file is used for Vercel deployment as it has reduced dependencies that install faster
- The `vercel.json` file configures Vercel to use `minimal_api.py` as the entry point
- Make sure your Qdrant instance is accessible from the internet if hosted externally
- The knowledge base must be populated BEFORE deploying to Vercel, as the process_book.py script may not run properly in Vercel's environment