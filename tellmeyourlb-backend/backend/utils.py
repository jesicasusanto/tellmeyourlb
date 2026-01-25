"""
CLIP text/image embedding via Hugging Face transformers (avoids torchvision/torch.dynamo issues).
"""
import torch
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPModel, AutoProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(MODEL_ID).to(device)
processor = AutoProcessor.from_pretrained(MODEL_ID)


def embed_text(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    return features / features.norm(dim=-1, keepdim=True)


def embed_image(image_bytes):
    image = Image.open(image_bytes).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    return features / features.norm(dim=-1, keepdim=True)


def embed_image_from_url(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            features = model.get_image_features(**inputs)
        return features[0].cpu().numpy().tolist()
    except Exception as e:
        print(f"Failed to process image {url}: {e}")
        return None
