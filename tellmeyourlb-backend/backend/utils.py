import torch
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPModel, AutoProcessor

MODEL_ID = "openai/clip-vit-base-patch32"

_device = "cpu"   # FORCE CPU — Render has no GPU
_model = None
_processor = None


def _load_model():
    global _model, _processor
    if _model is None or _processor is None:
        _model = CLIPModel.from_pretrained(MODEL_ID)
        _processor = AutoProcessor.from_pretrained(MODEL_ID)
        _model.eval()
    return _model, _processor


def embed_text(text: str):
    model, processor = _load_model()
    inputs = processor(text=[text], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    return features / features.norm(dim=-1, keepdim=True)


def embed_image_from_url(url: str):
    try:
        model, processor = _load_model()
        response = requests.get(url, timeout=5)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = model.get_image_features(**inputs)
        return features[0].cpu().numpy().tolist()
    except Exception as e:
        print(f"Image embedding failed: {e}")
        return None
