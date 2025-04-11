def match_products(expanded_terms: list, product_catalog: list, top_k: int = 10):
    """
    Match expanded query terms against product tags.
    Returns a ranked list of matching product dictionaries.
    """
    matched_products = []

    for product in product_catalog:
        # Combine name, category, and tags into a single searchable string
        searchable_text = (
            product["product_name"] + " " +
            product["product_category"] + " " +
            " ".join(product["tags"])
        ).lower()

        # Check how many expanded terms match
        score = sum(term.lower() in searchable_text for term in expanded_terms)

        if score > 0:
            product_copy = product.copy()
            product_copy["match_score"] = score
            matched_products.append(product_copy)

    # Sort by match score (descending)
    matched_products = sorted(matched_products, key=lambda x: x["match_score"], reverse=True)

    return matched_products[:top_k]
