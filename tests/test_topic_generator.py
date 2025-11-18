"""
Tests for Topic Generator Module
"""

import pytest
from unittest.mock import patch, MagicMock
from src.topic_generator import generate_topics, load_prompt

def test_load_prompt():
    """Test loading the prompt from file."""
    prompt = load_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "HCM" in prompt

@patch('src.topic_generator.client')
def test_generate_topics(mock_client):
    """Test topic generation with mocked OpenAI response."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "1. Topic One\n2. Topic Two\n3. Topic Three"
    mock_client.chat.completions.create.return_value = mock_response

    topics = generate_topics(3)

    assert len(topics) == 3
    assert "Topic One" in topics[0]
    mock_client.chat.completions.create.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])