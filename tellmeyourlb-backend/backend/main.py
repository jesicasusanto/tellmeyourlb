import json
from pathlib import Path
from utils import embed_text, embed_image_from_url

# Load brands: prefer data/indonesia.json, fallback to brands_raw.json
backend_dir = Path(__file__).resolve().parent
data_path = backend_dir / "../../data/indonesia.json"
raw_path = backend_dir / "brands_raw.json"

if data_path.exists():
    with open(data_path) as f:
        data = json.load(f)
    brands = data.get("data", data) if isinstance(data, dict) else data
    print(f"Loaded {len(brands)} brands from data/indonesia.json")
else:
    with open(raw_path) as f:
        data = json.load(f)
    brands = data.get("data", data) if isinstance(data, dict) else data
    print(f"Loaded {len(brands)} brands from brands_raw.json")

# Embed each brand's style description
for brand in brands:
    embedding = embed_text(brand["style_desc"])
    brand["embedding"] = embedding.cpu().numpy().tolist()[0]
    # brand["image_embedding"] = embed_image_from_url(brand["image"])

# Save to brands_embedded.json
with open(backend_dir / "brands_embedded.json", "w") as f:
    json.dump(brands, f, indent=2)

print("Saved brands_embedded.json")
