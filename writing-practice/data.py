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
        {"rumi": "kereta", "jawi": "كريتا", "english": "car"},
        {"rumi": "nasi", "jawi": "ناسي", "english": "rice"},
        {"rumi": "kucing", "jawi": "كوچيڠ", "english": "cat"},
        {"rumi": "makan", "jawi": "ماكن", "english": "eat"},
        {"rumi": "minum", "jawi": "مينوم", "english": "drink"},
        {"rumi": "tidur", "jawi": "تيدور", "english": "sleep"},
        {"rumi": "baca", "jawi": "باچ", "english": "read"},
    ]
