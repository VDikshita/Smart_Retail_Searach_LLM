from utils.text_utils import clean_text

def generate_suggestions(user_input: str, product_catalog: list, max_suggestions: int = 6) -> list:
    """
    Generates smart suggestions based on partial query.
    Matches against product names and tags (real-time as user types).
    """
    user_input = clean_text(user_input)
    suggestions = set()

    for product in product_catalog:
        name = clean_text(product["product_name"])
        tags = [clean_text(tag) for tag in product["tags"]]

        # If user input is a prefix of product name
        if user_input in name:
            suggestions.add(product["product_name"])

        # If user input matches part of any tag
        for tag in tags:
            if user_input in tag:
                suggestions.add(f"{tag} - {product['product_name']}")

        if len(suggestions) >= max_suggestions:
            break

    return list(suggestions)[:max_suggestions]
