import os

# Temporary fix to prevent SSL errors
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]


from groq import Groq  # pip install groq

#  Directly pass your Groq API key here (for local testing only)
groq_client = Groq(api_key="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")

#  Retail-specific tag list — restrict LLM output to these
RETAIL_TAGS = [
    "sneakers", "shoes", "sandals", "loafers", "heels", "boots", "flip-flops",
    "walking shoes", "formal shoes", "slippers", "trainers", "crocs", "slip-ons",
    "sports shoes", "casual shoes"
]

def get_synonyms_from_llm(query: str) -> list:
    prompt = f"""
You are a smart retail search assistant for a footwear store.
Given a user query, expand it to include synonyms, misspellings, slang, or alternate retail terms — 
but ONLY using this list of allowed product keywords:

{', '.join(RETAIL_TAGS)}

Query: "{query}"

Respond as a Python list of strings with no explanation. Example: ["sneakers", "sports shoes", "kicks"]
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100
        )
        text_output = response.choices[0].message.content.strip()

        #  Parse LLM output safely
        if text_output.startswith("["):
            synonyms = eval(text_output)
            return [s.lower() for s in synonyms if isinstance(s, str)]
        return []
    except Exception as e:
        print("LLM error:", e)
        return []
