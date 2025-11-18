"""
Editor Agent Module

This module refines and humanizes AI-generated blog post drafts.
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
    """Load the editor agent prompt from file."""
    try:
        with open('../prompts/editor_agent_prompt.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Editor agent prompt file not found.")
        raise

def edit_draft(draft):
    """
    Edit and refine a blog post draft.

    Args:
        draft (str): The original draft

    Returns:
        str: The edited draft in Markdown
    """
    try:
        prompt = load_prompt().format(draft=draft)

        response = client.chat.completions.create(
            model="grok-4-fast-non-reasoning",
            messages=[
                {"role": "system", "content": "You are an experienced editor for HCM blog content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )

        edited_draft = response.choices[0].message.content.strip()

        logger.info("Draft edited successfully.")
        return edited_draft
    except Exception as e:
        logger.error(f"Error editing draft: {e}")
        raise

# Example usage
if __name__ == "__main__":
    sample_draft = "In today's world, remote work is becoming more common..."
    edited = edit_draft(sample_draft)
    print(edited)