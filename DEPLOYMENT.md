# Clarifi Deployment Guide

## Quick Deploy (Vercel + Railway)

### Option A: Vercel (Frontend) + Railway (Backend)

#### 1. Deploy Frontend to Vercel

1. **Commit code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect Vercel**
   - Go to [vercel.com](https://vercel.com) → Import Project
   - Select your Clarifi GitHub repo
   - Install Vercel GitHub app if prompted
   - Click "Import"

3. **Configure Environment Variables in Vercel**
   - After import, go to Settings → Environment Variables
   - Add: `VITE_API_BASE_URL=https://clarifi-backend.railway.app` (replace with your actual Railway backend URL)
   - Click "Save"

4. **Deploy**
   - Click "Deploy"
   - Wait ~2-3 minutes, frontend is live at `https://clarifi-<random>.vercel.app`

#### 2. Deploy Backend to Railway

1. **Connect Railway**
   - Go to [railway.app](https://railway.app) → Create New Project → GitHub Repo
   - Select your Clarifi repo
   - Select "Python" as deployment environment
   - Click "Deploy Now"

2. **Configure Environment Variables in Railway**
   - After deployment starts, go to Project → Services → clarifi (backend)
   - Click "Variables"
   - Add these (from your [backend/.env](backend/.env)):
     ```
     SERPER_API_KEY=your_key_here
     OPENAI_API_KEY=your_key_here
     OPENAI_MODEL=gpt-4o-mini
     ```
   - Click "Save"

3. **Get Backend URL**
   - In Railway, go to Networking → Public Networking
   - Copy the generated URL (e.g., `https://clarifi-backend.railway.app`)
   - This is your VITE_API_BASE_URL for frontend

4. **Update Frontend with Backend URL**
   - Go back to Vercel Settings → Environment Variables
   - Update `VITE_API_BASE_URL` to Railway's URL from step 3
   - Trigger redeploy (or just push a commit)

---

### Option B: Docker Deploy (Self-Hosted / Cloud Run / etc.)

Build both images locally and push to Docker Hub:

```bash
# Build backend
docker build -t yourusername/clarifi-backend:latest ./backend
docker push yourusername/clarifi-backend:latest

# Build frontend (requires Nginx)
docker build -t yourusername/clarifi-frontend:latest .
docker push yourusername/clarifi-frontend:latest

# Then deploy to your cloud provider
```

---

## Environment Variables Needed

**Frontend** ([vercel.json](vercel.json)):
- `VITE_API_BASE_URL` — backend URL (e.g., https://clarifi-backend.railway.app)

**Backend** ([backend/railway.toml](backend/railway.toml) or Railway console):
- `SERPER_API_KEY` — from [serper.dev](https://serper.dev)
- `OPENAI_API_KEY` — from [platform.openai.com](https://platform.openai.com/api-keys)
- `OPENAI_MODEL` — default: `gpt-4o-mini`

---

## After Deployment

1. **Test health endpoint**:
   ```bash
   curl https://clarifi-backend.railway.app/health
   ```
   Should return: `{"status":"ok"}`

2. **Open frontend**:
   - Visit `https://clarifi-<random>.vercel.app`
   - Try uploading a resume or asking a market question
   - Results should come from live backend + Serper search

3. **Check Logs**
   - Vercel: Deployments → select latest → Logs
   - Railway: Services → clarifi → Logs

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `CORS error` in browser | Check backend CORS middleware allows frontend domain |
| `API_BASE_URL undefined` | Verify `VITE_API_BASE_URL` env var in Vercel |
| Backend 500 error | Check Railway env vars (SERPER_API_KEY, OPENAI_API_KEY) are set |
| File upload fails | Ensure backend has write permissions (Railway auto-handles this) |

---

## Next Steps

- Monitor backend logs regularly (Railroad console)
- Set up email alerts for failures (Railway dashboard)
- Consider adding APM/monitoring (Sentry, DataDog, etc.)
- Plan database if you want persistent resume history

