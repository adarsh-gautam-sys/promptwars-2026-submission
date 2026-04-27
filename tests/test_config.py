"""
Unit tests for the Settings/Config module.
Tests environment variable parsing, defaults, and CORS origin handling.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from config import Settings


class TestSettingsDefaults:
    """Test that default settings are correctly applied."""

    def test_default_model(self):
        settings = Settings(GEMINI_API_KEY="test-key")
        assert settings.gemini_model == "gemini-2.5-flash"

    def test_default_port(self):
        settings = Settings(GEMINI_API_KEY="test-key")
        assert settings.port == 8000

    def test_default_host(self):
        settings = Settings(GEMINI_API_KEY="test-key")
        assert settings.host == "0.0.0.0"

    def test_default_rate_limit(self):
        settings = Settings(GEMINI_API_KEY="test-key")
        assert settings.max_requests_per_minute == 20

    def test_api_key_accepts_custom_value(self):
        settings = Settings(GEMINI_API_KEY="custom-test-key")
        assert settings.gemini_api_key == "custom-test-key"


class TestCORSParsing:
    """Test CORS origin string to list parsing."""

    def test_default_cors_origins(self):
        settings = Settings(GEMINI_API_KEY="test-key")
        origins = settings.cors_origin_list
        assert isinstance(origins, list)
        assert len(origins) >= 3

    def test_custom_cors_origins(self):
        settings = Settings(
            GEMINI_API_KEY="test-key",
            CORS_ORIGINS="https://example.com,https://other.com"
        )
        origins = settings.cors_origin_list
        assert "https://example.com" in origins
        assert "https://other.com" in origins

    def test_cors_handles_whitespace(self):
        settings = Settings(
            GEMINI_API_KEY="test-key",
            CORS_ORIGINS="https://a.com , https://b.com "
        )
        origins = settings.cors_origin_list
        assert "https://a.com" in origins
        assert "https://b.com" in origins

    def test_cors_empty_string(self):
        settings = Settings(GEMINI_API_KEY="test-key", CORS_ORIGINS="")
        origins = settings.cors_origin_list
        assert origins == []


class TestSettingsOverrides:
    """Test that environment overrides work correctly."""

    def test_custom_port(self):
        settings = Settings(GEMINI_API_KEY="test-key", PORT=9000)
        assert settings.port == 9000

    def test_custom_model(self):
        settings = Settings(GEMINI_API_KEY="test-key", GEMINI_MODEL="gemini-2.0-flash")
        assert settings.gemini_model == "gemini-2.0-flash"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
