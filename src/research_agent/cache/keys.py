import hashlib
import re


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.lower()).strip()


def semantic_cache_key(query: str) -> str:
    digest = hashlib.sha256(normalize_query(query).encode()).hexdigest()[:24]
    return f"semantic:{digest}"
