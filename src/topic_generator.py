"""
Topic Generator Module

This module generates HCM blog topic ideas using AI.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_prompt():
    """Load the topic generation prompt from file."""
    with open('../prompts/topic_generation_prompt.txt', 'r') as f:
        return f.read()

def generate_topics(num_topics=5):
    """
    Generate blog topic ideas for HCM.

    Args:
        num_topics (int): Number of topics to generate

    Returns:
        list: List of generated topic strings
    """
    prompt = load_prompt().format(num_topics=num_topics)

    response = client.chat.completions.create(
        model="gpt-4",
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

    return topics

# Example usage
if __name__ == "__main__":
    topics = generate_topics(3)
    for topic in topics:
        print(topic)