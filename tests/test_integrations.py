"""
Integration Tests for Blog Pipeline

Tests x.ai API integration and Nextcloud file uploads.
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from config/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

from src.topic_generator import generate_topics
from src.scheduler import upload_to_nextcloud

def test_xai_integration():
    """Test x.ai API integration for topic generation."""
    # Skip if no API key
    if not os.getenv('XAI_API_KEY'):
        pytest.skip("XAI_API_KEY not set")

    try:
        topics = generate_topics(3, mode='research')
        assert isinstance(topics, list)
        assert len(topics) >= 3
        print(f"Generated topics: {topics}")
    except Exception as e:
        pytest.fail(f"x.ai integration failed: {e}")

def test_nextcloud_upload():
    """Test Nextcloud file upload integration."""
    # Skip if credentials not set
    required_env = ['NEXTCLOUD_URL', 'NEXTCLOUD_USERNAME', 'NEXTCLOUD_PASSWORD']
    if not all(os.getenv(key) for key in required_env):
        pytest.skip("Nextcloud credentials not set")

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content for Nextcloud upload")
        temp_file = f.name

    try:
        # Test upload to Blog directory
        remote_path = "Blog/test_upload.txt"
        upload_to_nextcloud(temp_file, remote_path)
        print(f"Successfully uploaded {temp_file} to {remote_path}")
    except Exception as e:
        pytest.fail(f"Nextcloud upload failed: {e}")
    finally:
        # Clean up temp file
        os.unlink(temp_file)

if __name__ == "__main__":
    pytest.main([__file__])