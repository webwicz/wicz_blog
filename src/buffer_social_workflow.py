"""
Buffer Social Workflow Module

This module automates social media posting via Buffer API by reading new blog posts from RSS feeds,
generating teaser snippets, and scheduling posts on LinkedIn and X/Twitter.
"""

import os
import logging
import requests
import feedparser
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize x.ai client for snippet generation
client = OpenAI(api_key=os.getenv('XAI_API_KEY'), base_url="https://api.x.ai/v1")

def parse_rss_feed(feed_url, last_checked=None):
    """
    Parse the RSS feed and return new posts since last_checked.

    Args:
        feed_url (str): URL of the RSS feed
        last_checked (datetime): Last time we checked for new posts

    Returns:
        list: List of new post dictionaries with title, link, description, published
    """
    try:
        feed = feedparser.parse(feed_url)
        new_posts = []

        for entry in feed.entries:
            published = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()

            if last_checked is None or published > last_checked:
                post = {
                    'title': entry.title,
                    'link': entry.link,
                    'description': entry.description if hasattr(entry, 'description') else '',
                    'published': published
                }
                new_posts.append(post)

        logger.info(f"Found {len(new_posts)} new posts from RSS.")
        return new_posts
    except Exception as e:
        logger.error(f"Error parsing RSS feed: {e}")
        raise

def generate_teaser_snippet(title, description, link):
    """
    Generate a short teaser snippet using AI.

    Args:
        title (str): Post title
        description (str): Post description
        link (str): Post URL

    Returns:
        str: Teaser snippet
    """
    prompt = f"""
    Create a short, engaging teaser for this blog post:

    Title: {title}
    Description: {description[:500]}...

    The teaser should:
    - Be 100-150 characters
    - Spark interest
    - End with a call to read more
    - Include the link: {link}
    """

    try:
        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are a social media copywriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        snippet = response.choices[0].message.content.strip()
        logger.info("Teaser snippet generated.")
        return snippet
    except Exception as e:
        logger.error(f"Error generating teaser: {e}")
        # Fallback to simple format
        return f"Check out: {title} {link}"

def format_buffer_post(title, link, teaser):
    """
    Format the post content for Buffer.

    Args:
        title (str): Post title
        link (str): Post URL
        teaser (str): Teaser snippet

    Returns:
        str: Formatted post text
    """
    return f"{teaser}\n\n{title}\n{link}"

def schedule_buffer_post(content, platforms, delay_minutes=60):
    """
    Schedule a post via Buffer API.

    Args:
        content (str): Post content
        platforms (list): List of platform IDs (e.g., ['linkedin', 'twitter'])
        delay_minutes (int): Minutes to delay posting

    Returns:
        dict: Buffer API response
    """
    try:
        access_token = os.getenv('BUFFER_ACCESS_TOKEN')
        if not access_token:
            raise ValueError("BUFFER_ACCESS_TOKEN not set")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Get user profiles
        profiles_response = requests.get('https://api.bufferapp.com/1/profiles.json', headers=headers)
        profiles_response.raise_for_status()
        profiles = profiles_response.json()

        # Map platforms to profile IDs
        platform_ids = []
        for profile in profiles:
            if profile['service'].lower() in [p.lower() for p in platforms]:
                platform_ids.append(profile['id'])

        if not platform_ids:
            raise ValueError("No matching profiles found for platforms")

        # Calculate schedule time
        schedule_time = datetime.utcnow() + timedelta(minutes=delay_minutes)
        schedule_iso = schedule_time.isoformat() + 'Z'

        data = {
            'text': content,
            'profile_ids': platform_ids,
            'scheduled_at': schedule_iso
        }

        response = requests.post('https://api.bufferapp.com/1/updates/create.json', json=data, headers=headers)
        response.raise_for_status()

        result = response.json()
        logger.info(f"Post scheduled via Buffer: {result['id']}")
        return result
    except Exception as e:
        logger.error(f"Error scheduling Buffer post: {e}")
        raise

def run_social_workflow(feed_url=None, platforms=['linkedin', 'twitter'], delay_minutes=60, last_checked_file='../data/last_checked.txt'):
    """
    Main workflow: Check RSS, process new posts, schedule social media posts.

    Args:
        feed_url (str): RSS feed URL (from env if None)
        platforms (list): Platforms to post to
        delay_minutes (int): Delay before posting
        last_checked_file (str): File to store last checked time
    """
    try:
        feed_url = feed_url or os.getenv('RSS_FEED_URL')
        if not feed_url:
            raise ValueError("RSS_FEED_URL not set")

        # Load last checked time
        last_checked = None
        if os.path.exists(last_checked_file):
            with open(last_checked_file, 'r') as f:
                last_checked_str = f.read().strip()
                if last_checked_str:
                    last_checked = datetime.fromisoformat(last_checked_str)

        # Parse RSS for new posts
        new_posts = parse_rss_feed(feed_url, last_checked)

        for post in new_posts:
            # Generate teaser
            teaser = generate_teaser_snippet(post['title'], post['description'], post['link'])

            # Format post
            buffer_content = format_buffer_post(post['title'], post['link'], teaser)

            # Schedule via Buffer
            result = schedule_buffer_post(buffer_content, platforms, delay_minutes)

            logger.info(f"Scheduled post for: {post['title']}")

        # Update last checked time
        with open(last_checked_file, 'w') as f:
            f.write(datetime.now().isoformat())

        logger.info("Social workflow completed successfully.")
    except Exception as e:
        logger.error(f"Social workflow failed: {e}")
        raise

# Example usage
if __name__ == "__main__":
    run_social_workflow()