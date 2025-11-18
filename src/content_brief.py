"""
Content Brief Module

This module creates structured outlines for blog posts using AI.
"""

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize x.ai client
client = OpenAI(api_key=os.getenv('XAI_API_KEY'), base_url="https://api.x.ai/v1")

def load_prompt():
    """Load the content brief prompt from file."""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'content_brief_prompt.txt')
        with open(prompt_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Content brief prompt file not found.")
        raise

def create_brief(topic):
    """
    Create a content brief for a given topic.

    Args:
        topic (str): The blog post topic

    Returns:
        str: The generated content brief
    """
    try:
        prompt = load_prompt().format(topic=topic)

        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are a content strategist for HCM blogs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.6
        )

        brief = response.choices[0].message.content.strip()

        logger.info(f"Created brief for topic: {topic}")
        return brief
    except Exception as e:
        logger.error(f"Error creating brief: {e}")
        raise

# Example usage
if __name__ == "__main__":
    brief = create_brief("The Future of Remote Work in HCM")
    print(brief)