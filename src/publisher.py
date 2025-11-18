"""
Publisher Module

This module publishes blog posts to Medium.
"""

import os
import logging
from dotenv import load_dotenv
from medium import Client

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

def publish_to_medium(title, content, tags=None, publish_status='draft'):
    """
    Publish a blog post to Medium.

    Args:
        title (str): Post title
        content (str): Post content in Markdown
        tags (list): List of tags
        publish_status (str): 'draft' or 'public'

    Returns:
        str: Post URL or success message
    """
    try:
        integration_token = os.getenv('MEDIUM_INTEGRATION_TOKEN')
        if not integration_token:
            raise ValueError("MEDIUM_INTEGRATION_TOKEN not set")

        client = Client(access_token=integration_token)
        user = client.get_current_user()

        post = client.create_post(
            user_id=user['id'],
            title=title,
            content=content,
            content_format='markdown',
            tags=tags or ['HCM', 'HR', 'Thought Leadership'],
            publish_status=publish_status
        )

        logger.info(f"Post published to Medium: {post['url']}")
        return post['url']
    except Exception as e:
        logger.error(f"Error publishing to Medium: {e}")
        raise

def publish_post(content, platform='medium', title='HCM Blog Post', tags=None, status='draft'):
    """
    Publish a blog post to the specified platform.

    Args:
        content (str): The full post content in Markdown
        platform (str): Platform to publish to ('medium')
        title (str): Post title
        tags (list): Tags for the post
        status (str): Publication status

    Returns:
        str: Success message or URL
    """
    if platform == 'medium':
        # Extract title from content if not provided separately
        lines = content.split('\n')
        if not title or title == 'HCM Blog Post':
            title = lines[0].strip('# ')  # Assume first line is # Title
            content_body = '\n'.join(lines[1:])  # Rest is body
        else:
            content_body = content

        return publish_to_medium(title, content_body, tags, status)
    else:
        logger.warning(f"Publishing to {platform} not implemented yet")
        return f"Publishing to {platform} not implemented yet"

# Example usage
if __name__ == "__main__":
    sample_content = "# Sample HCM Post\n\nThis is a test post about HCM trends."
    result = publish_post(sample_content, status='draft')
    print(result)