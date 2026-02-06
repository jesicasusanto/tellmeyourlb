from sentence_transformers import SentenceTransformer
import torch

_model = None

def load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )
        _model.eval()
    return _model

def embed_text(text: str):
    model = load_model()
    with torch.no_grad():
        emb = model.encode(
            text,
            normalize_embeddings=True
        )
    return emb.tolist()
