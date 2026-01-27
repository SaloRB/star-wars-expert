"""End-to-end integration tests for the RAG chain.

These tests use the real vectorstore and OpenAI model to validate
that the system can correctly answer Star Wars questions.

Run with: uv run pytest tests/test_rag_integration.py -v -m integration
"""

import pytest
from langchain_core.documents import Document

from vectorstore import get_or_create_vectorstore
from chat import create_rag_chain
from config import LLM_MODEL


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def rag_chain():
    """Create a RAG chain with the real vectorstore.
    
    This fixture is module-scoped to avoid recreating the vectorstore
    for each test, which would be slow and expensive.
    """
    from dotenv import load_dotenv
    from rich.console import Console
    
    load_dotenv()  # Load OPENAI_API_KEY from .env
    
    console = Console(quiet=True)  # Suppress output during tests
    vectorstore = get_or_create_vectorstore(console)
    chain, memory = create_rag_chain(vectorstore)
    return chain


class TestStarWarsQuestions:
    """Test that the RAG chain can answer Star Wars questions correctly."""

    def test_luke_skywalker_identity(self, rag_chain):
        """Test that the system knows who Luke Skywalker is."""
        response = ""
        for chunk in rag_chain.stream("Who is Luke Skywalker?"):
            response += chunk
        
        assert len(response) > 50, "Response should be substantial"
        assert "luke" in response.lower(), "Response should mention Luke"
        # Luke is the main protagonist
        assert any(word in response.lower() for word in ["hero", "jedi", "skywalker", "farm", "tatooine"])

    def test_darth_vader_identity(self, rag_chain):
        """Test that the system knows who Darth Vader is."""
        response = ""
        for chunk in rag_chain.stream("Who is Darth Vader?"):
            response += chunk
        
        assert len(response) > 50, "Response should be substantial"
        assert "vader" in response.lower(), "Response should mention Vader"

    def test_famous_quote_i_am_your_father(self, rag_chain):
        """Test knowledge of the famous 'I am your father' scene."""
        response = ""
        for chunk in rag_chain.stream("What does Vader say to Luke about his father?"):
            response += chunk
        
        assert len(response) > 50, "Response should be substantial"
        # Should reference the father revelation
        assert "father" in response.lower(), "Response should mention 'father'"

    def test_movie_identification(self, rag_chain):
        """Test that the system can identify which movie events occur in."""
        response = ""
        for chunk in rag_chain.stream("In which movie does Luke destroy the Death Star?"):
            response += chunk
        
        assert len(response) > 30, "Response should be substantial"
        # Should mention A New Hope or Episode IV
        assert any(phrase in response.lower() for phrase in ["new hope", "episode iv", "first"])

    def test_character_dialogue(self, rag_chain):
        """Test that the system can quote character dialogue."""
        response = ""
        for chunk in rag_chain.stream("What does Obi-Wan say about the Force?"):
            response += chunk
        
        assert len(response) > 50, "Response should be substantial"
        assert "force" in response.lower(), "Response should discuss the Force"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_non_starwars_question(self, rag_chain):
        """Test response to a non-Star Wars question."""
        response = ""
        for chunk in rag_chain.stream("What is the capital of France?"):
            response += chunk
        
        assert len(response) > 10, "Should provide some response"
        # Should still be polite and redirect to Star Wars
        assert "paris" in response.lower() or "star wars" in response.lower()

    def test_greeting(self, rag_chain):
        """Test response to a simple greeting."""
        response = ""
        for chunk in rag_chain.stream("Hello!"):
            response += chunk
        
        assert len(response) > 5, "Should respond to greeting"

    def test_unknown_character(self, rag_chain):
        """Test response about a character not in the original trilogy."""
        response = ""
        for chunk in rag_chain.stream("Who is Jar Jar Binks?"):
            response += chunk
        
        # Jar Jar is NOT in the original trilogy, so it should indicate lack of info
        assert len(response) > 20, "Should provide some response"
