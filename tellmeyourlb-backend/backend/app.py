import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import embed_text

_backend_dir = Path(__file__).resolve().parent
with open(_backend_dir / "brands_embedded.json") as f:
    brands = json.load(f)

def cosine_similarity(vec1, vec2):
    vec1 = np.asarray(vec1, dtype=np.float32)
    vec2 = np.asarray(vec2, dtype=np.float32)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_best_matches(input_embedding: List[float], brands: List[Dict], top_k=5):
    scores = []
    for brand in brands:
        score = cosine_similarity(input_embedding, brand["embedding"]).item()
        scores.append({
            "score": float(score),
            "name": brand["name"],
            "style_desc": brand["style_desc"],
            "instagram": brand.get("instagram", ""),
            "image": brand.get("image", "")
        })
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_k]

app = FastAPI(
    title="Brand Recommendation API",
    description="Finds the most similar fashion brands based on style description",
    version="1.0.0"
)

_raw = os.getenv("CORS_ORIGINS", "").strip()
_origins = [o.strip() for o in _raw.split(",") if o.strip()] if _raw else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/recommend")
def recommend_brands(request: QueryRequest):
    text_features = embed_text(request.query)
    input_embedding = text_features.cpu().numpy().tolist()[0]
    matches = find_best_matches(input_embedding, brands, top_k=request.top_k)

    return {"query": request.query, "results": matches}

@app.get("/health")
def health_check():
    return {"status": "ok"}
