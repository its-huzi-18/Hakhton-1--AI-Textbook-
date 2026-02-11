# Vercel Deployment Checklist

## Pre-deployment Verification

- [x] All dependencies installed (`pip install -r requirements.txt`)
- [x] Dependencies compatible with Python 3.9 (as specified in runtime.txt)
- [x] Vercel configuration files present (`vercel.json`, `vercel_app.py`, `minimal_api.py`)
- [x] Environment variables documented and ready to be set
- [x] API endpoints tested and functional
- [x] Chatbot functionality verified
- [x] CORS configuration set up for frontend integration

## Required Environment Variables

- [ ] `COHERE_API_KEY` - Your Cohere API key
- [ ] `QDRANT_URL` - Your Qdrant cluster URL
- [ ] `QDRANT_API_KEY` - Your Qdrant API key
- [ ] `FRONTEND_ORIGIN` - Your frontend domain (optional)

## Deployment Steps

1. [ ] Choose deployment method (Vercel CLI or Git integration)
2. [ ] Set root directory to `backend` if using Git integration
3. [ ] Add environment variables to Vercel project settings
4. [ ] Deploy the backend service
5. [ ] Test API endpoints after deployment
6. [ ] Connect frontend to deployed backend
7. [ ] Test end-to-end functionality

## Post-deployment Verification

- [ ] Backend API is accessible at deployed URL
- [ ] `/health` endpoint returns healthy status
- [ ] `/status` endpoint shows environment is configured
- [ ] `/ask` and `/query` endpoints are available
- [ ] Frontend can communicate with backend
- [ ] Chatbot responds to queries appropriately

## Rollback Plan

If deployment fails:
1. Check Vercel logs for specific error messages
2. Verify environment variables are correctly set
3. Confirm all required files are included in deployment
4. Revert to previous working version if needed