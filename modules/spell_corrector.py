from symspellpy.symspellpy import SymSpell, Verbosity
import os

# Manual overrides for domain-specific words
MANUAL_CORRECTIONS = {
    "sniker": "sneakers",
    "chapal": "chappal",
    "lofars": "loafers",
    "slipers": "slippers",
    "sneker": "sneakers",
    "snekerz": "sneakers"
}

# Initialize SymSpell (optional if you still want fallback)
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
DICTIONARY_PATH = "data/frequency_dictionary_en_82_765.txt"

if os.path.exists(DICTIONARY_PATH):
    sym_spell.load_dictionary(DICTIONARY_PATH, term_index=0, count_index=1)

def correct_spelling(user_query: str) -> str:
    query = user_query.strip().lower()

    # Manual fix first
    if query in MANUAL_CORRECTIONS:
        return MANUAL_CORRECTIONS[query]

    # Optional: fallback to SymSpell
    suggestions = sym_spell.lookup(query, Verbosity.CLOSEST, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term

    return query  # fallback to raw input
