"""
Draft Writer Module

This module generates first drafts of blog posts using AI.
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
    """Load the draft writer prompt from file."""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'draft_writer_prompt.txt')
        with open(prompt_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Draft writer prompt file not found.")
        raise

def write_draft(brief):
    """
    Write a blog post draft based on a content brief.

    Args:
        brief (str): The content brief

    Returns:
        str: The generated blog post draft in Markdown
    """
    try:
        prompt = load_prompt().format(brief=brief)

        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are a professional blog writer for HCM topics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.8
        )

        draft = response.choices[0].message.content.strip()

        logger.info("Draft written successfully.")
        return draft
    except Exception as e:
        logger.error(f"Error writing draft: {e}")
        raise

# Example usage
if __name__ == "__main__":
    sample_brief = "Objective: Educate HR professionals on remote work trends..."
    draft = write_draft(sample_brief)
    print(draft)