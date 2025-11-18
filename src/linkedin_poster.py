"""
LinkedIn Poster Module

This module posts snippets to LinkedIn.
"""

import os
import logging
from dotenv import load_dotenv
from linkedin_api import Linkedin

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

def post_to_linkedin(content, title=None):
    """
    Post a snippet to LinkedIn.

    Args:
        content (str): The post content
        title (str): Optional title

    Returns:
        str: Success message
    """
    try:
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        if not email or not password:
            raise ValueError("LinkedIn credentials not set")

        api = Linkedin(email, password)

        # Post text
        post = api.create_post(content)

        logger.info("Posted to LinkedIn successfully.")
        return "Posted to LinkedIn"
    except Exception as e:
        logger.error(f"Error posting to LinkedIn: {e}")
        raise

def generate_linkedin_snippet(draft, max_length=300):
    """
    Generate a LinkedIn snippet from the draft.

    Args:
        draft (str): The full draft
        max_length (int): Max length of snippet

    Returns:
        str: Snippet
    """
    # Extract first paragraph or summary
    lines = draft.split('\n')
    snippet = ""
    for line in lines:
        if line.strip() and not line.startswith('#'):
            snippet += line + " "
            if len(snippet) > max_length:
                break
    snippet = snippet[:max_length].strip() + "... #HCM #HR #ThoughtLeadership"
    return snippet

# Example usage
if __name__ == "__main__":
    snippet = generate_linkedin_snippet("# Title\n\nThis is the content.")
    print(snippet)