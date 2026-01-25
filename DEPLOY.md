# Deploy Gaya (Tell Me Your LB) for Your Resume

Deploy the **frontend** and **backend** so you can share a live link. Do these in order: push to GitHub, deploy backend, deploy frontend.

---

## 1. Push to GitHub

From the project root (`tellmeyourlb/`):

```bash
cd ~/Desktop/Personal/website/tellmeyourlb

# If you don't have a git repo yet:
git init

# Add everything (node_modules, venv, .env are ignored via .gitignore)
git add .
git commit -m "Initial commit: Gaya – Indonesian fashion brand recommender"

# Create a new repo on GitHub (github.com → New repository, e.g. "tellmeyourlb").
# Then:
git remote add origin https://github.com/YOUR_USERNAME/tellmeyourlb.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. If the repo already exists, use:

```bash
git remote add origin https://github.com/YOUR_USERNAME/tellmeyourlb.git
git push -u origin main
```

---

## 2. Deploy the backend (Render)

The API uses **FastAPI + PyTorch + transformers**. Render’s free tier has 512MB RAM; it can be tight. If it runs out of memory, use a paid plan or Railway.

1. Go to [render.com](https://render.com) and sign in (GitHub is fine).
2. **New → Web Service**.
3. Connect the `tellmeyourlb` repo.
4. Set:

   | Field | Value |
   |-------|--------|
   | **Name** | `gaya-api` (or any name) |
   | **Root Directory** | `tellmeyourlb-backend/backend` |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |

5. **Plan**: Free (or paid if you hit memory limits).
6. Under **Environment**, add:
   - `CORS_ORIGINS` = `https://your-frontend.vercel.app`  
     (you can add this after the frontend is deployed; until then you can leave it blank – the app allows `*` when `CORS_ORIGINS` is not set).
7. Create the service. The first deploy can take 10–15 minutes (installing torch/transformers).
8. Copy the service URL, e.g. `https://gaya-api.onrender.com` — this is your **backend URL**.

If the service crashes with an out-of-memory error, switch to a paid instance or try [Railway](https://railway.app) and run the same commands there.

---

## 3. Deploy the frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. **Add New → Project** and import the `tellmeyourlb` repo.
3. Configure:

   | Field | Value |
   |-------|--------|
   | **Root Directory** | `indo-brands` (click Edit and set it) |
   | **Framework Preset** | Vite |
   | **Build Command** | `npm run build` (default) |
   | **Output Directory** | `dist` (default) |

4. Under **Environment Variables**, add:

   | Name | Value |
   |------|--------|
   | `VITE_API_URL` | `https://gaya-api.onrender.com` (your backend URL from step 2) |

   Apply it to Production (and Preview if you want).

5. Deploy. Vercel will give you a URL like `https://tellmeyourlb.vercel.app`.

6. **(Optional)** Add the Vercel URL to the backend’s `CORS_ORIGINS` on Render:
   - Render → your backend service → Environment → `CORS_ORIGINS` = `https://tellmeyourlb.vercel.app`  
   (If you left `CORS_ORIGINS` empty, the backend already allows all origins, so this is optional.)

---

## 4. Resume link

Use the **frontend** URL as the demo link, e.g.:

**https://tellmeyourlb.vercel.app**

(Replace with your real Vercel URL.)

That page talks to your deployed backend; no extra setup for recruiters.

---

## Alternatives

- **Frontend:** [Netlify](https://netlify.com) — same idea: root `indo-brands`, build `npm run build`, publish `dist`, set `VITE_API_URL`.
- **Backend:** [Railway](https://railway.app) — New Project → Deploy from GitHub → root `tellmeyourlb-backend/backend`, build `pip install -r requirements.txt`, start `uvicorn app:app --host 0.0.0.0 --port $PORT`. Railway’s free tier can be more forgiving with memory than Render’s.

---

## Checklist

- [ ] Repo pushed to GitHub
- [ ] Backend deployed and `/health` returns `{"status":"ok"}`
- [ ] Frontend deployed with `VITE_API_URL` = backend URL
- [ ] In the app, a test query returns brand cards
- [ ] Frontend URL saved for your resume
