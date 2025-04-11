import re

def clean_text(text: str) -> str:
    """
    Lowercases and removes special characters from a string.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()

def tokenize(text: str) -> list:
    """
    Splits text into words.
    """
    return clean_text(text).split()
