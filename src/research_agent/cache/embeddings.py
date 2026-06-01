import math
from collections import Counter

from research_agent.cache.keys import normalize_query


def embed_text(text: str) -> Counter[str]:
    return Counter(normalize_query(text).split())


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    words = set(left) | set(right)
    dot = sum(left[word] * right[word] for word in words)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return round(dot / (left_norm * right_norm), 4)
