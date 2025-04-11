from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utils.load_data import load_product_catalog
from llm.llm_utils import get_synonyms_from_llm
from modules.spell_corrector import correct_spelling
from modules.product_matcher import match_products

# Initialize FastAPI app
app = FastAPI(title="Smart Retail Search")

# Enable CORS so frontend dev can call it from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with Django app origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your actual product catalog from JSON
product_catalog = load_product_catalog()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search_products(query: str = Query(..., min_length=1)):
    # Step 1: Fix typos if any
    corrected = correct_spelling(query)

    # Step 2: Expand using LLM (Groq-powered)
    synonyms = get_synonyms_from_llm(corrected)

    # Step 3: Match against product catalog
    matched = match_products(synonyms, product_catalog)

    return {
        "corrected_query": corrected,
        "expanded_terms": synonyms,
        "matched_products": matched
    }
