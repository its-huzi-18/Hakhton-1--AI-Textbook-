# Vercel Deployment Guide for AI Textbook Chatbot

## Overview
This guide explains how to deploy your RAG chatbot to Vercel. The backend is designed to work seamlessly with Vercel's serverless functions.

## Prerequisites

### 1. Required Accounts
- [Vercel Account](https://vercel.com/)
- [Cohere API Key](https://dashboard.cohere.com/api-keys)
- [Qdrant Cloud Account](https://cloud.qdrant.io/) (or self-hosted Qdrant instance)

### 2. Environment Variables
Before deploying, you'll need these environment variables:

```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here (e.g., https://your-cluster-id.qdrant.tech:6333)
QDRANT_API_KEY=your_qdrant_api_key_here
FRONTEND_ORIGIN=https://your-frontend-domain.vercel.app (optional, defaults to hakhton-ai-textbook.vercel.app)
```

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Navigate to your project directory:
```bash
cd D:\Vs Code-All-Things\Github Repo\Hakhton-1( AI Textbook)\backend
```

3. Login to Vercel:
```bash
vercel login
```

4. Deploy the backend:
```bash
vercel --cwd .
```

5. During deployment, add your environment variables when prompted, or add them later in the Vercel dashboard.

### Option 2: Deploy via Git Integration

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)

2. Go to [Vercel Dashboard](https://vercel.com/dashboard)

3. Click "Add New Project" and import your repository

4. In the project settings:
   - Set the Root Directory to `backend`
   - Add the required environment variables in the "Environment Variables" section

5. Click "Deploy"

## Important Files for Vercel

The following files in the `backend` directory are specifically designed for Vercel deployment:

- `vercel.json` - Vercel configuration file
- `vercel_app.py` - Main application entry point for Vercel
- `minimal_api.py` - Lightweight API version for Vercel
- `requirements.txt` - Python dependencies

## Frontend Integration

Your frontend (likely in the main directory) should be deployed separately to Vercel. The frontend will communicate with the backend API at the deployed backend URL.

Update your frontend to use the correct backend API URL:
```javascript
const BACKEND_URL = process.env.BACKEND_URL || 'https://your-backend-deployment-url.vercel.app';
```

## Troubleshooting

### Common Issues:

1. **"Dependencies not installed" error**: Make sure your `requirements.txt` file includes all necessary packages:
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   python-dotenv==1.0.0
   pydantic>=1.10.13,<2.0.0
   cohere>=4.0.0
   qdrant-client>=1.8.0
   requests==2.31.0
   beautifulsoup4==4.12.2
   ```

2. **Environment variables not found**: Ensure you've added all required environment variables in the Vercel dashboard under Project Settings > Environment Variables.

3. **CORS errors**: The API is configured to allow requests from common origins. If you're still having CORS issues, check that your `FRONTEND_ORIGIN` environment variable is set correctly.

### Testing Your Deployment:

Once deployed, test these endpoints:
- `GET /` - Should return a welcome message
- `GET /health` - Should return health status
- `GET /status` - Should show environment configuration status

## Knowledge Base Setup

After deploying your backend, you'll need to populate your knowledge base. This typically involves:

1. Running the `process_book.py` script to index your book content into Qdrant
2. This can be done by triggering a special endpoint or running the script in your deployment environment

## Support

If you encounter issues during deployment:

1. Check the Vercel deployment logs in your dashboard
2. Verify all environment variables are correctly set
3. Ensure your Qdrant cluster is accessible from the internet
4. Confirm your Cohere API key is valid and has sufficient quota

## Notes

- The backend is designed to gracefully handle cases where environment variables aren't set, showing helpful error messages to users
- The API includes proper CORS configuration to work with frontend applications
- Serverless functions have timeout limitations, so complex operations are optimized for quick responses