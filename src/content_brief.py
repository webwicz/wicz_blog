"""
Content Brief Module

This module creates structured outlines for blog posts using AI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt():
    """Load the content brief prompt from file."""
    with open('../prompts/content_brief_prompt.txt', 'r') as f:
        return f.read()

def create_brief(topic):
    """
    Create a content brief for a given topic.

    Args:
        topic (str): The blog post topic

    Returns:
        str: The generated content brief
    """
    prompt = load_prompt().format(topic=topic)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a content strategist for HCM blogs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.6
    )

    brief = response.choices[0].message.content.strip()

    return brief

# Example usage
if __name__ == "__main__":
    brief = create_brief("The Future of Remote Work in HCM")
    print(brief)