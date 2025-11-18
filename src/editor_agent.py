"""
Editor Agent Module

This module refines and humanizes AI-generated blog post drafts.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt():
    """Load the editor agent prompt from file."""
    with open('../prompts/editor_agent_prompt.txt', 'r') as f:
        return f.read()

def edit_draft(draft):
    """
    Edit and refine a blog post draft.

    Args:
        draft (str): The original draft

    Returns:
        str: The edited draft
    """
    prompt = load_prompt().format(draft=draft)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an experienced editor for HCM blog content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.5
    )

    edited_draft = response.choices[0].message.content.strip()

    return edited_draft

# Example usage
if __name__ == "__main__":
    sample_draft = "In today's world, remote work is becoming more common..."
    edited = edit_draft(sample_draft)
    print(edited)