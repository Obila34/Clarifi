# ✅ Clarifi Deployment Checklist

## Pre-Deployment (Do This First)

- [ ] Verify all tests pass locally
  ```bash
  # Terminal A: Backend
  cd backend && source .venv/bin/activate && uvicorn app.main:app --port 8000
  
  # Terminal B: Frontend
  npm run dev
  
  # Terminal C: Test API
  curl -s http://localhost:8000/health
  ```

- [ ] Commit all changes
  ```bash
  git add .
  git commit -m "Ready for production deployment"
  git push origin main
  ```

---

## Deployment Steps (Vercel + Railway)

### Step 1: Deploy Backend (5 minutes)

1. Open [railway.app](https://railway.app)
2. Click **"Create New Project"** → **"Deploy from GitHub Repo"**
3. Select your Clarifi repository
4. Click **"Deploy Now"**
5. Wait for build to complete (~3-5 min)
6. Once deployed:
   - Go to **"Networking"** tab
   - Enable **"Public Networking"**
   - Copy the URL (e.g., `https://clarifi-backend.railway.app`)
   - **Save this URL** — you'll need it for frontend config

7. Add backend environment variables:
   - Click **"Variables"** tab
   - Add these keys from your [backend/.env](backend/.env):
     - `SERPER_API_KEY` = `your_key`
     - `OPENAI_API_KEY` = `your_key`
     - `OPENAI_MODEL` = `gpt-4o-mini`
   - Click **"Save"**

8. Test backend health:
   ```bash
   curl https://clarifi-backend.railway.app/health
   ```
   Should return: `{"status":"ok"}`

### Step 2: Deploy Frontend (5 minutes)

1. Open [vercel.com](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. Select your Clarifi GitHub repository
4. Click **"Import"**
5. In **"Environment Variables"** section, add:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://clarifi-backend.railway.app` (from Step 1)
6. Click **"Deploy"**
7. Wait for build (~2-3 min)
8. Once live, your frontend URL will be shown (e.g., `https://clarifi-xyz.vercel.app`)

---

## Post-Deployment Verification

- [ ] Frontend loads without errors
  - Visit your Vercel URL
  - Check browser console (F12) for errors
  
- [ ] Backend is responding
  ```bash
  curl https://clarifi-backend.railway.app/health
  ```

- [ ] Frontend can reach backend
  - In UI, try asking a market question
  - Should see real Serper search results
  - No "API failed" fallback messages

- [ ] Resume upload works
  - Test upload endpoint via UI
  - Verify resume parsing and ATS rewrites appear

- [ ] Gap Bridge works
  - Upload a resume
  - Click "Gap Bridge"
  - See learning resource cards

---

## Troubleshooting

**Frontend shows "API failed"**
- Check that `VITE_API_BASE_URL` in Vercel env matches your Railway backend URL
- Redeploy frontend after env change

**Backend 500 errors**
- Check Railway logs: Services → clarifi → Logs
- Verify `SERPER_API_KEY` and `OPENAI_API_KEY` are set in Railway Variables

**CORS errors in console**
- Backend CORS is pre-configured for localhost + production
- If deploying to different domain, update [backend/app/main.py](backend/app/main.py) `allow_origins`

**Resume upload returns 400**
- Check file size < 10MB
- Supported formats: PDF, DOCX, TXT only

---

## What's Deployed

| Component | Platform | URL | Status |
|-----------|----------|-----|--------|
| Frontend | Vercel | `https://clarifi-xyz.vercel.app` | ✅ |
| Backend API | Railway | `https://clarifi-backend.railway.app` | ✅ |
| Database | In-Memory (Railway) | N/A | ✅ Transient |

---

## Next Steps (Optional Enhancements)

1. **Add monitoring** → Sentry for error tracking
2. **Add logging** → LogRocket for frontend issues
3. **Add database** → Railway PostgreSQL for resume history
4. **Add caching** → Redis on Railway for speed
5. **Add rate limiting** → Slow down API abuse

---

## Rolling Back (If Needed)

**Vercel**: 
- Deployments → select previous version → Promote to Production

**Railway**:
- Services → Image → select previous tag → Deploy

---

**You're live! 🚀**
