# import streamlit as st
# from modules.spell_corrector import correct_spelling
# from modules.query_expansion import expand_query
# from modules.product_matcher import match_products
# from modules.product_display import display_product_grid
# from utils.load_data import load_product_catalog
# from modules.suggestion_engine import generate_suggestions

# #  Load product catalog
# product_catalog = load_product_catalog()

# #  Page layout
# st.set_page_config(page_title="Smart Retail Search", layout="wide")
# st.title(" Smart Retail Search")

# Ensure session variable exists
# if "search_input" not in st.session_state:
#     st.session_state.search_input = ""

# #  Search Input + Auto rerun on key change
# st.text_input(
#     "Search for products...",
#     key="search_input",
#     on_change=st.rerun  # Triggers rerun on every keystroke
# )

# #  Get user input from session
# user_input = st.session_state.search_input

# #  Live Suggestions While Typing
# if user_input and len(user_input) >= 2:
#     suggestions = generate_suggestions(user_input, product_catalog)
#     if suggestions:
#         st.markdown("###  Suggestions:")
#         for suggestion in suggestions:
#             if st.button(suggestion):
#                 st.session_state.search_input = suggestion
#                 st.rerun()
#         st.markdown("---")

# #  Trigger full search only when enough characters
# if user_input and len(user_input) >= 3:
#     #  Step 1: Spell correct
#     corrected_query = correct_spelling(user_input)
#     st.success(f" Corrected Query: `{corrected_query}`")

#     #  Step 2: Synonym Expansion (LLM + tag filter)
#     expanded_terms = expand_query(corrected_query)
#     st.info(f" Expanded Terms: {', '.join(expanded_terms)}")

#     #  Step 3: Product Match
#     matched_products = match_products(expanded_terms, product_catalog)

#     #  Step 4: Show Results
#     if matched_products:
#         st.markdown("##  Matching Products")
#         display_product_grid(matched_products, columns=2)
#     else:
#         st.warning(" No exact match. Showing popular alternatives:")
#         display_product_grid(product_catalog[:4], columns=2)

import os

# ✅ Fix SSL_CERT_FILE issue
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
