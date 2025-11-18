"""
Publisher Module

This module publishes blog posts to platforms like WordPress or Ghost.
"""

import os
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

def publish_to_wordpress(title, content, status='draft'):
    """
    Publish a blog post to WordPress.

    Args:
        title (str): Post title
        content (str): Post content
        status (str): Post status ('draft', 'publish')

    Returns:
        str: Post ID or success message
    """
    wp_url = os.getenv('WORDPRESS_URL')
    wp_username = os.getenv('WORDPRESS_USERNAME')
    wp_password = os.getenv('WORDPRESS_PASSWORD')

    client = Client(wp_url, wp_username, wp_password)

    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = status

    post_id = client.call(NewPost(post))

    return f"Post published with ID: {post_id}"

def publish_post(content, platform='wordpress', title='HCM Blog Post', status='draft'):
    """
    Publish a blog post to the specified platform.

    Args:
        content (str): The full post content (including title if needed)
        platform (str): Platform to publish to ('wordpress', 'ghost')
        title (str): Post title
        status (str): Publication status

    Returns:
        str: Success message
    """
    if platform == 'wordpress':
        # Extract title from content if not provided separately
        lines = content.split('\n')
        if not title or title == 'HCM Blog Post':
            title = lines[0].strip('# ')  # Assume first line is # Title
            content_body = '\n'.join(lines[1:])  # Rest is body
        else:
            content_body = content

        return publish_to_wordpress(title, content_body, status)
    else:
        return f"Publishing to {platform} not implemented yet"

# Example usage
if __name__ == "__main__":
    sample_content = "# Sample HCM Post\n\nThis is a test post about HCM trends."
    result = publish_post(sample_content, status='draft')
    print(result)