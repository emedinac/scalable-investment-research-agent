from dataclasses import dataclass
from typing import Any

from research_agent.cache.embeddings import cosine_similarity, embed_text
from research_agent.cache.keys import semantic_cache_key
from research_agent.core.config import Settings


@dataclass
class CacheLookup:
    hit: bool
    key: str
    value: Any | None = None
    similarity: float | None = None


class SemanticCache:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._memory: dict[str, tuple[str, Any]] = {}

    async def get(self, query: str) -> CacheLookup:
        key = semantic_cache_key(query)
        if key in self._memory:
            return CacheLookup(hit=True, key=key, value=self._memory[key][1], similarity=1.0)

        query_embedding = embed_text(query)
        best_key: str | None = None
        best_similarity = 0.0
        best_value: Any | None = None
        for cached_key, (cached_query, cached_value) in self._memory.items():
            similarity = cosine_similarity(query_embedding, embed_text(cached_query))
            if similarity > best_similarity:
                best_key = cached_key
                best_similarity = similarity
                best_value = cached_value

        if best_key and best_similarity >= self.settings.semantic_cache_threshold:
            return CacheLookup(hit=True, key=best_key, value=best_value, similarity=best_similarity)
        return CacheLookup(hit=False, key=key)

    async def set(self, query: str, value: Any) -> str:
        key = semantic_cache_key(query)
        self._memory[key] = (query, value)
        return key
