import json
from pathlib import Path
from utils import embed_text  # Make sure this uses the correct model

# Paths
backend_dir = Path(__file__).resolve().parent
raw_path = backend_dir / "brands_raw.json"
embedded_path = backend_dir / "brands_embedded.json"

# Load raw brands
with open(raw_path, "r") as f:
    brands_data = json.load(f)["data"]

# Generate embeddings
for brand in brands_data:
    brand["embedding"] = embed_text(brand["style_desc"])

# Save new embedded JSON
with open(embedded_path, "w") as f:
    json.dump(brands_data, f, indent=4)

print(f"Saved {len(brands_data)} brand embeddings to {embedded_path}")
