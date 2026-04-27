"""
ElectionGuide AI — Response Cache Module
Simple in-memory TTL cache for avoiding redundant Gemini API calls.
Tool responses are static (election rules don't change), so caching is safe.
"""

import time
import hashlib
import logging

logger = logging.getLogger("electionguide.cache")


class ResponseCache:
    """Thread-safe in-memory cache with TTL expiration."""

    def __init__(self, ttl: int = 86400, max_size: int = 500):
        """
        Args:
            ttl: Time-to-live in seconds (default: 24 hours)
            max_size: Maximum number of cached entries
        """
        self._cache: dict[str, tuple[dict, float]] = {}
        self._ttl = ttl
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def _make_key(self, message: str) -> str:
        """Normalize and hash the message for consistent cache keys."""
        normalized = message.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()

    def get(self, message: str) -> dict | None:
        """Retrieve a cached response if it exists and hasn't expired."""
        key = self._make_key(message)
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                self._hits += 1
                logger.info("Cache HIT for key %s (hits=%d)", key[:8], self._hits)
                return value
            # Expired — remove it
            del self._cache[key]
        self._misses += 1
        return None

    def set(self, message: str, response: dict) -> None:
        """Store a response in the cache."""
        # Evict oldest entries if at capacity
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]

        key = self._make_key(message)
        self._cache[key] = (response, time.time())
        logger.info("Cache SET for key %s (size=%d)", key[:8], len(self._cache))

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def stats(self) -> dict:
        """Return cache statistics."""
        total = self._hits + self._misses
        return {
            "size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{(self._hits / total * 100):.1f}%" if total > 0 else "N/A",
        }


# Singleton cache instance — 24 hour TTL, max 500 entries
response_cache = ResponseCache(ttl=86400, max_size=500)
