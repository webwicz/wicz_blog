"""
Draft Writer Module

This module generates first drafts of blog posts using AI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt():
    """Load the draft writer prompt from file."""
    with open('../prompts/draft_writer_prompt.txt', 'r') as f:
        return f.read()

def write_draft(brief):
    """
    Write a blog post draft based on a content brief.

    Args:
        brief (str): The content brief

    Returns:
        str: The generated blog post draft
    """
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

    return draft

# Example usage
if __name__ == "__main__":
    sample_brief = "Objective: Educate HR professionals on remote work trends..."
    draft = write_draft(sample_brief)
    print(draft)