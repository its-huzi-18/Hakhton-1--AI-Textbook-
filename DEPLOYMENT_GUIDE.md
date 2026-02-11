# Deployment Guide for RAG Chatbot

## Backend Deployment Options

### Option A: Railway (Recommended for initial setup)

#### Prerequisites
- Railway account
- Access to Qdrant vector database
- Cohere API key

#### Environment Variables Required
Set these environment variables in your Railway project:

```
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_url
COHERE_API_KEY=your_cohere_api_key
TARGET_URL=https://your-frontend-url.vercel.app  # The URL of your deployed frontend
PORT=8000
```

#### Deployment Steps
1. Connect your GitHub repository to Railway
2. Set the environment variables as listed above
3. Railway will automatically use the `railway.toml` configuration
4. The backend will be deployed and accessible at the Railway URL

#### Populate Knowledge Base (Required)
After the first deployment, you need to populate the knowledge base:
1. Run the `process_book.py` script once to populate the vector database:
   ```bash
   python process_book.py
   ```

### Option B: Vercel (For production backend)

#### Prerequisites
- Vercel account
- Access to Qdrant vector database (must be accessible from the internet)
- Cohere API key
- Knowledge base already populated in Qdrant

#### Environment Variables Required
Set these environment variables in your Vercel project dashboard:

```
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url (e.g., https://your-cluster-id.region.cloud.qdrant.io:6333)
QDRANT_API_KEY=your_qdrant_api_key
TARGET_URL=https://your-frontend-domain.vercel.app
```

#### Deployment Steps
1. Push your updated code to GitHub (with the corrected requirements.txt)
2. Connect your repository to Vercel
3. During project setup, select the `/backend` directory as the root
4. Set the environment variables in Vercel dashboard
5. Redeploy from the Vercel dashboard

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account

### Environment Variables Required
Set these environment variables in your Vercel project for the frontend:

```
RAG_CHATBOT_API_URL=https://your-backend-url.vercel.app  # If backend is on Vercel
# OR
RAG_CHATBOT_API_URL=https://your-backend-url.up.railway.app  # If backend is on Railway
NEXT_PUBLIC_RAG_CHATBOT_API_URL=${RAG_CHATBOT_API_URL}
```

### Deployment Steps
1. Connect your GitHub repository to Vercel
2. Select the `my-book` directory as the project root
3. Set the environment variables as listed above
4. Vercel will automatically build and deploy the Docusaurus site

## Configuration Notes

### API Endpoints
- Main: `GET /` - Basic health check
- Health: `GET /health` - Detailed health check
- Status: `GET /status` - Environment configuration status
- Ask: `POST /ask` (for frontend chatbot)
- Query: `POST /query` (for more detailed queries)
- Collections: `GET /collections` - List available collections

### CORS Settings
The backend allows all origins for development. In production, update api.py to restrict origins.

## Troubleshooting

### Common Issues
1. **CORS errors**: Make sure the frontend can access the backend API
2. **Empty responses**: Ensure the knowledge base has been populated in Qdrant
3. **API key errors**: Verify all API keys are correctly set in environment variables
4. **"Service not configured"**: Missing environment variables in deployment
5. **"Dependencies not installed"**: requirements.txt missing required packages

### Testing the Deployment
1. Verify the backend is running: `GET /` should return a success message
2. Check environment: `GET /status` should show `environment_configured: true`
3. Verify health: `GET /health` should return status healthy
4. Test the ask endpoint with a sample question
5. Check that the frontend chatbot can communicate with the backend

### Debugging Steps
1. Check the `/status` endpoint to see if environment variables are properly set
2. Verify your Qdrant connection by checking if collections are returned
3. Test the `/ask` endpoint directly with a simple POST request
4. Check Vercel logs for any import or runtime errors