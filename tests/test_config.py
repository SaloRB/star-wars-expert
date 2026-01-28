"""Tests for the config module."""

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    LLM_MODEL,
    LLM_TEMPERATURE,
    MAX_RETRIES,
    PERSIST_PATH,
    PROMPT_TEMPLATE,
    REQUEST_TIMEOUT,
    RETRIEVER_K,
    RETRY_BACKOFF_FACTOR,
    STAR_WARS_SCRIPTS,
)


class TestConfigConstants:
    """Tests for configuration constants."""

    def test_persist_path_is_string(self):
        """Test that PERSIST_PATH is a valid string."""
        assert isinstance(PERSIST_PATH, str)
        assert len(PERSIST_PATH) > 0

    def test_collection_name_is_string(self):
        """Test that COLLECTION_NAME is a valid string."""
        assert isinstance(COLLECTION_NAME, str)
        assert len(COLLECTION_NAME) > 0

    def test_llm_model_is_valid(self):
        """Test that LLM_MODEL is a non-empty string.

        Note: Actual model validation is done by the OpenAI API at runtime.
        See https://platform.openai.com/docs/models for valid models.
        """
        assert isinstance(LLM_MODEL, str)
        assert len(LLM_MODEL) > 0

    def test_llm_temperature_in_valid_range(self):
        """Test that LLM_TEMPERATURE is within valid range [0, 2]."""
        assert isinstance(LLM_TEMPERATURE, (int, float))
        assert 0 <= LLM_TEMPERATURE <= 2

    def test_retriever_k_is_positive(self):
        """Test that RETRIEVER_K is a positive integer."""
        assert isinstance(RETRIEVER_K, int)
        assert RETRIEVER_K > 0

    def test_chunk_size_is_positive(self):
        """Test that CHUNK_SIZE is a positive integer."""
        assert isinstance(CHUNK_SIZE, int)
        assert CHUNK_SIZE > 0

    def test_chunk_overlap_less_than_size(self):
        """Test that CHUNK_OVERLAP is less than CHUNK_SIZE."""
        assert isinstance(CHUNK_OVERLAP, int)
        assert CHUNK_OVERLAP >= 0
        assert CHUNK_OVERLAP < CHUNK_SIZE

    def test_request_timeout_is_positive(self):
        """Test that REQUEST_TIMEOUT is a positive number."""
        assert isinstance(REQUEST_TIMEOUT, (int, float))
        assert REQUEST_TIMEOUT > 0

    def test_max_retries_is_positive(self):
        """Test that MAX_RETRIES is a positive integer."""
        assert isinstance(MAX_RETRIES, int)
        assert MAX_RETRIES > 0

    def test_retry_backoff_factor_is_positive(self):
        """Test that RETRY_BACKOFF_FACTOR is a positive number."""
        assert isinstance(RETRY_BACKOFF_FACTOR, (int, float))
        assert RETRY_BACKOFF_FACTOR > 0


class TestStarWarsScripts:
    """Tests for STAR_WARS_SCRIPTS configuration."""

    def test_scripts_is_list(self):
        """Test that STAR_WARS_SCRIPTS is a list."""
        assert isinstance(STAR_WARS_SCRIPTS, list)

    def test_scripts_not_empty(self):
        """Test that STAR_WARS_SCRIPTS is not empty."""
        assert len(STAR_WARS_SCRIPTS) > 0

    def test_each_script_has_required_fields(self):
        """Test that each script entry has title and url."""
        for script in STAR_WARS_SCRIPTS:
            assert "title" in script
            assert "url" in script
            assert isinstance(script["title"], str)
            assert isinstance(script["url"], str)

    def test_scripts_have_valid_urls(self):
        """Test that script URLs start with http."""
        for script in STAR_WARS_SCRIPTS:
            assert script["url"].startswith("http")


class TestPromptTemplate:
    """Tests for PROMPT_TEMPLATE configuration."""

    def test_prompt_template_is_string(self):
        """Test that PROMPT_TEMPLATE is a string."""
        assert isinstance(PROMPT_TEMPLATE, str)

    def test_prompt_template_has_context_placeholder(self):
        """Test that PROMPT_TEMPLATE contains {context} placeholder."""
        assert "{context}" in PROMPT_TEMPLATE

    def test_prompt_template_has_question_placeholder(self):
        """Test that PROMPT_TEMPLATE contains {question} placeholder."""
        assert "{question}" in PROMPT_TEMPLATE
