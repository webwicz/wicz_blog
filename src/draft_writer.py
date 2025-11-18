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

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt():
    """Load the draft writer prompt from file."""
    try:
        with open('../prompts/draft_writer_prompt.txt', 'r') as f:
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
            model="gpt-4",
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