"""
Topic Generator Module

This module generates HCM blog topic ideas using AI.
"""

import os
import logging
from datetime import datetime
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

def generate_topics(num_topics=5, mode='research'):
    """
    Generate blog topic ideas for HCM.

    Args:
        num_topics (int): Number of topics to generate
        mode (str): 'research' for weekly research, 'report' for tri-weekly report

    Returns:
        list or str: List of topics or report content
    """
    try:
        prompt = load_prompt().format(num_topics=num_topics)

        if mode == 'research':
            # Weekly research mode: generate broad topics
            prompt += "\n\nFocus on emerging trends, challenges, and opportunities in HCM for the coming week."
        elif mode == 'report':
            # Tri-weekly report mode: select and prioritize topics
            prompt += "\n\nProvide a curated report of the top 3-5 topics to draft articles about this week, with brief rationale for each."

        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are an expert HCM content strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000 if mode == 'research' else 1500,
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        if mode == 'research':
            # Parse into list
            topics = [line.strip() for line in content.split('\n') if line.strip() and line[0].isdigit()]
            logger.info(f"Generated {len(topics)} research topics.")
            return topics
        elif mode == 'report':
            # Return formatted report
            report = f"# HCM Topic Report - {datetime.now().strftime('%Y-%m-%d')}\n\n{content}"
            logger.info("Generated topic report.")
            return report

    except Exception as e:
        logger.error(f"Error generating topics: {e}")
        raise

# Example usage
if __name__ == "__main__":
    topics = generate_topics(3)
    for topic in topics:
        print(topic)