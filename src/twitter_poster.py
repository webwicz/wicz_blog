"""
Twitter Poster Module

This module posts snippets to Twitter (X).
"""

import os
import logging
from dotenv import load_dotenv
import tweepy

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

def post_to_twitter(content):
    """
    Post a snippet to Twitter.

    Args:
        content (str): The post content

    Returns:
        str: Success message
    """
    try:
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        if not all([api_key, api_secret, access_token, access_token_secret]):
            raise ValueError("Twitter credentials not set")

        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        tweet = api.update_status(content)

        logger.info(f"Posted to Twitter: {tweet.id}")
        return "Posted to Twitter"
    except Exception as e:
        logger.error(f"Error posting to Twitter: {e}")
        raise

def generate_twitter_snippet(draft, max_length=280):
    """
    Generate a Twitter snippet from the draft.

    Args:
        draft (str): The full draft
        max_length (int): Max length of snippet

    Returns:
        str: Snippet
    """
    # Extract title and first sentence
    lines = draft.split('\n')
    title = lines[0].strip('# ')
    first_para = ""
    for line in lines[1:]:
        if line.strip() and not line.startswith('#'):
            first_para = line.strip()
            break
    snippet = f"{title}: {first_para[:max_length - len(title) - 3]}... #HCM #HR"
    return snippet[:max_length]

# Example usage
if __name__ == "__main__":
    snippet = generate_twitter_snippet("# Title\n\nThis is the content.")
    print(snippet)