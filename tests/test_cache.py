"""
Unit tests for the ResponseCache module.
Tests cache operations: set/get, TTL expiry, eviction, key normalization, and stats.
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from cache import ResponseCache


class TestCacheBasicOperations:
    """Test basic cache get/set operations."""

    def test_set_and_get(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("Hello world", {"response": "Hi!"})
        result = cache.get("Hello world")
        assert result is not None
        assert result["response"] == "Hi!"

    def test_get_missing_key(self):
        cache = ResponseCache(ttl=60, max_size=10)
        result = cache.get("nonexistent query")
        assert result is None

    def test_key_normalization_case_insensitive(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("How do I REGISTER to vote?", {"response": "steps"})
        result = cache.get("how do i register to vote?")
        assert result is not None
        assert result["response"] == "steps"

    def test_key_normalization_whitespace(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("  hello  ", {"response": "world"})
        result = cache.get("hello")
        assert result is not None


class TestCacheTTL:
    """Test TTL (time-to-live) expiration behavior."""

    def test_expired_entry_returns_none(self):
        cache = ResponseCache(ttl=1, max_size=10)  # 1 second TTL
        cache.set("test", {"response": "data"})
        time.sleep(1.1)  # Wait for expiry
        result = cache.get("test")
        assert result is None

    def test_fresh_entry_returns_value(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("test", {"response": "data"})
        result = cache.get("test")
        assert result is not None


class TestCacheEviction:
    """Test cache eviction when max_size is reached."""

    def test_evicts_oldest_when_full(self):
        cache = ResponseCache(ttl=60, max_size=2)
        cache.set("first", {"response": "1"})
        time.sleep(0.01)  # Ensure different timestamps
        cache.set("second", {"response": "2"})
        time.sleep(0.01)
        cache.set("third", {"response": "3"})  # Should evict "first"

        assert cache.get("first") is None
        assert cache.get("second") is not None
        assert cache.get("third") is not None

    def test_max_size_respected(self):
        cache = ResponseCache(ttl=60, max_size=3)
        for i in range(10):
            cache.set(f"query_{i}", {"response": str(i)})
        assert cache.stats["size"] <= 3


class TestCacheStats:
    """Test cache statistics tracking."""

    def test_initial_stats(self):
        cache = ResponseCache(ttl=60, max_size=10)
        stats = cache.stats
        assert stats["size"] == 0
        assert stats["hits"] == 0
        assert stats["misses"] == 0

    def test_hit_tracking(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("test", {"response": "data"})
        cache.get("test")
        cache.get("test")
        assert cache.stats["hits"] == 2

    def test_miss_tracking(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.get("nonexistent")
        cache.get("also_missing")
        assert cache.stats["misses"] == 2

    def test_clear_resets_stats(self):
        cache = ResponseCache(ttl=60, max_size=10)
        cache.set("test", {"response": "data"})
        cache.get("test")
        cache.clear()
        stats = cache.stats
        assert stats["size"] == 0
        assert stats["hits"] == 0
        assert stats["misses"] == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
