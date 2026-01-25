# tellmeyourlb-backend

Backend for the Indonesian local fashion brand recommender (Gaya). Uses **Hugging Face transformers** (CLIP) to embed style descriptions and cosine similarity to recommend brands.

---

## Setup

1. **Create a virtualenv and install dependencies**

   ```bash
   cd tellmeyourlb-backend/backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Use the venv’s Python so `torch` is installed in the right place:

   ```bash
   ./venv/bin/python -m pip install -r requirements.txt
   ```

2. **If you see `ModuleNotFoundError: No module named 'torch._dynamo.resume_execution'`**

   Downgrade to a known-good torch/torchvision:

   ```bash
   pip install 'torch==2.6.0' 'torchvision==0.21.0'
   ```

   `requirements.txt` uses `torch>=2.6` and `torchvision>=0.21`; if 2.7.x causes issues on your Mac (Python 3.12 + arm64), pin to 2.6.0 and 0.21.0.

3. **Build embeddings from your dataset**

   Uses `data/indonesia.json` if it exists, otherwise `brands_raw.json`:

   ```bash
   # from tellmeyourlb-backend/backend, with venv activated
   python main.py
   ```

   This creates/overwrites `brands_embedded.json`. Re-run when you change the dataset.

---

## Run the backend

From `tellmeyourlb-backend/backend`, **use the venv’s Python** so it finds `torch` and the rest of the deps:

```bash
source venv/bin/activate
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or without activating (same effect):

```bash
./venv/bin/python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

If you see `ModuleNotFoundError: No module named 'torch'` when running uvicorn, the command is using system Python instead of the venv. Use `python -m uvicorn` with the venv activated, or `./venv/bin/python -m uvicorn` as above.

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- `POST /recommend` body: `{ "query": "minimal streetwear", "top_k": 5 }`

---

## Run the frontend

From the project root, in a **new terminal**:

```bash
cd indo-brands
npm install   # first time only
npm run dev
```

The app will be at `http://localhost:5173` (or the next free port Vite suggests). It calls the backend at `http://localhost:8000` by default.

To use a different backend URL:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

---

## Run backend + frontend together

1. **Terminal 1 – backend**

   ```bash
   cd tellmeyourlb-backend/backend
   source venv/bin/activate
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Terminal 2 – frontend**

   ```bash
   cd indo-brands
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser, describe your style in the input, and click send (or press Enter) to get brand recommendations.
