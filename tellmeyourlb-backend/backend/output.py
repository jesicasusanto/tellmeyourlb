import numpy as np
from typing import List, Dict
from utils import embed_text
import json
def cosine_similarity(vec1, vec2):
    vec1 = np.asarray(vec1, dtype=np.float32)
    vec2 = np.asarray(vec2, dtype=np.float32)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_best_matches(input_embedding: List[float], brands: List[Dict], top_k=5):
    scores = []
    for brand in brands:
        score = cosine_similarity(input_embedding, brand["embedding"]).item()
        scores.append((score, brand["name"], brand["style_desc"]))
    scores.sort(reverse=True)
    return scores[:top_k]



# Assume you embed this with the same model
input_embedding = embed_text("clothes too big, comfortable, simple, non formal, casual")
  # Replace with your actual model call
# Load your JSON
with open("brands_embedded.json") as f:
    brands = json.load(f)

# Embed each brand’s style description
    #brand["image_embedding"] = embed_image_from_url(brand["image"])
# Get top 3 matches
matches = find_best_matches(input_embedding, brands, top_k=3)

for score, name, desc in matches:
    print(f"{name} ({score:.4f}): {desc}")
