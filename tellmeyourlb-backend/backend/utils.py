from sentence_transformers import SentenceTransformer
import torch
import numpy as np

_model = None

def load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )
        _model.eval()
        # Convert model weights to float16 to save memory
        _model.half()
    return _model

def embed_text(text: str):
    model = load_model()
    # Disable gradients to avoid unnecessary memory usage
    with torch.no_grad():
        emb = model.encode(text, normalize_embeddings=True)
    # Return as float32 list for JSON compatibility
    return emb.astype(np.float32).tolist()
