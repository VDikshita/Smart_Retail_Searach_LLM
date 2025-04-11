from llm.llm_utils import get_synonyms_from_llm
from utils.load_data import load_product_catalog, load_synonym_dict

# Static fallback synonyms (optional)
STATIC_SYNONYMS = load_synonym_dict()
PRODUCT_CATALOG = load_product_catalog()

def expand_query(user_query: str) -> list:
    query = user_query.strip().lower()

    #  1. Load from static dictionary (manual bootstrapped)
    static_terms = STATIC_SYNONYMS.get(query, [])

    #  2. Get dynamic synonyms from LLM (Groq)
    dynamic_terms = get_synonyms_from_llm(query)

    #  3. Filter LLM synonyms to match only product names or tags in dataset
    matched_terms = set()
    for term in dynamic_terms:
        for product in PRODUCT_CATALOG:
            if term in product["product_name"].lower() or any(term in tag.lower() for tag in product["tags"]):
                matched_terms.add(term)
                break

    #  4. Combine everything
    final_terms = set([query] + static_terms + list(matched_terms))
    return list(final_terms)
