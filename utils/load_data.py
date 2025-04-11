import json
import os

def load_product_catalog(file_path="data/product_catalog.json"):
    """Load the product catalog from JSON."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Product catalog not found at {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_synonym_dict(file_path="data/synonym_dict.json"):
    """Load synonym dictionary if it exists (fallback for LLM)."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
