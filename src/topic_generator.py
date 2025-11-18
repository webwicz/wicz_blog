"""
Topic Generator Module

This module generates HCM blog topic ideas using AI.
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
    """Load the topic generation prompt from file."""
    try:
        with open('../prompts/topic_generation_prompt.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Topic generation prompt file not found.")
        raise

def generate_topics(num_topics=5):
    """
    Generate blog topic ideas for HCM.

    Args:
        num_topics (int): Number of topics to generate

    Returns:
        list: List of generated topic strings
    """
    try:
        prompt = load_prompt().format(num_topics=num_topics)

        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are an expert HCM content strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        topics_text = response.choices[0].message.content.strip()
        # Parse the response into a list (assuming numbered list)
        topics = [line.strip() for line in topics_text.split('\n') if line.strip() and line[0].isdigit()]

        logger.info(f"Generated {len(topics)} topics.")
        return topics
    except Exception as e:
        logger.error(f"Error generating topics: {e}")
        raise

# Example usage
if __name__ == "__main__":
    topics = generate_topics(3)
    for topic in topics:
        print(topic)