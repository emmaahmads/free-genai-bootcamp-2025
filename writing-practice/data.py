from typing import List, TypedDict

class Word(TypedDict):
    rumi: str
    jawi: str
    english: str

def fetch_words() -> List[Word]:
    """Fetch the word collection."""
    # In a real application, this would call an API
    return [
        {"rumi": "buku", "jawi": "بوكو", "english": "book"},
    ]

