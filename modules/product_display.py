def render_products_html(products):
    """
    Converts a list of product dicts into HTML cards for display in Gradio.
    """
    if not products:
        return "<p>No matching products found.</p>"

    html = "<div style='display:flex; flex-wrap:wrap; gap:20px;'>"

    for p in products:
        html += f"""
        <div style='border:1px solid #ddd; border-radius:10px; padding:10px; width:200px; text-align:center;'>
            <img src="{p['image_link']}" style="width:180px; height:180px; object-fit:cover; border-radius:6px;"><br>
            <b>{p['product_name']}</b><br>
            <small>Category: <code>{p['product_category']}</code></small><br>
            <strong>₹{p['product_price']}</strong>
        </div>
        """

    html += "</div>"
    return html
