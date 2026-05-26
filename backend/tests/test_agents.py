import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage
from backend.agents.research_agent import run_research_agent

@patch("backend.agents.research_agent.DuckDuckGoSearchResults")
@patch("backend.agents.research_agent.ChatGroq")
def test_research_agent_returns_data(mock_chat_groq_class, mock_search_class):
    mock_search = MagicMock()
    mock_search.invoke.return_value = "Mocked search results about Machine Learning."
    mock_search_class.return_value = mock_search

    mock_llm_instance = MagicMock()
    # Return a mocked AIMessage with JSON output that the parser expects
    expected_json = '{"topic": "Machine Learning", "key_concepts": ["Algorithm"], "facts": ["Subfield of AI"], "sources": ["https://ml.org"]}'
    mock_llm_instance.invoke.return_value = AIMessage(content=expected_json)
    mock_chat_groq_class.return_value = mock_llm_instance

    data = run_research_agent("Machine Learning")
    
    assert data["topic"] == "Machine Learning"
    assert "Algorithm" in data["key_concepts"]
    assert "Subfield of AI" in data["facts"]
    assert "https://ml.org" in data["sources"]

def test_research_agent_exception_fallback():
    # Test that exception fallback returns the expected dict
    with patch("backend.agents.research_agent.DuckDuckGoSearchResults") as mock_search_class:
        mock_search = MagicMock()
        # Trigger an exception during execution
        mock_search.invoke.side_effect = Exception("Search API failed")
        mock_search_class.return_value = mock_search
        
        data = run_research_agent("Test fallback")
        
        assert data["topic"] == "Test fallback"
        assert len(data["key_concepts"]) == 0
        assert "Error extracting data: Search API failed" in data["facts"][0]
