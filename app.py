
import os

#  Fix SSL_CERT_FILE issue
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]

import gradio as gr
from modules.spell_corrector import correct_spelling
from modules.query_expansion import expand_query
from modules.product_matcher import match_products
from modules.product_display import render_products_html  # new helper
from utils.load_data import load_product_catalog

# Load product catalog
product_catalog = load_product_catalog()

def smart_search(query):
    if not query or len(query) < 2:
        return "", ""

    corrected = correct_spelling(query)
    expanded_terms = expand_query(corrected)
    matches = match_products(expanded_terms, product_catalog)

    suggestions_display = f"🔍 Corrected: `{corrected}`\n\n Expanded Terms: {', '.join(expanded_terms)}"
    product_html = render_products_html(matches if matches else product_catalog[:4])
    
    return suggestions_display, product_html

iface = gr.Interface(
    fn=smart_search,
    inputs=gr.Textbox(placeholder="Search shoes, sneakers, sandals...", lines=1, label="🔎 Smart Product Search"),
    outputs=[
        gr.Textbox(label="LLM Suggestions"),
        gr.HTML(label=" Products")
    ],
    live=True,
    title="Smart Retail Search (Gradio)",
    description="Get product suggestions with AI-powered query expansion."
)

if __name__ == "__main__":
    iface.launch()
