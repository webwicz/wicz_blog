# HCM Thought-Leadership Blog Pipeline

## Project Overview

This project is an AI-assisted blogging system focused on Human Capital Management (HCM), industry trends, and best practices. It provides a modular pipeline for generating blog topics, creating content briefs, drafting articles, editing for human-like quality, publishing to Medium, and amplifying on social media (LinkedIn and X/Twitter).

The system is designed to support thought-leadership content creation without product promotion, leveraging AI agents to streamline the blogging process. Content is stored in Markdown locally for version control.

## Features

- **Topic Generation**: AI-powered generation of relevant HCM blog topics based on current trends.
- **Content Briefing**: Structured outlines for blog posts with SEO and structure focus.
- **Draft Writing**: Automated first drafts using AI, output in Markdown.
- **Editing**: Refinement and humanization of AI-generated text, preserving Markdown.
- **Medium Publishing**: Direct export to Medium via API.
- **Social Amplification**: Automated posting of snippets to LinkedIn and X/Twitter.
- **Analytics**: Collection of engagement metrics from Medium and social platforms.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/webwicz/wicz_blog.git
   cd wicz_blog
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `config/.env.template` to `config/.env`
   - Fill in your API keys (OpenAI, Medium, Twitter, LinkedIn)

## Usage

### Running the Pipeline

1. Generate topics:
   ```python
   from src.topic_generator import generate_topics

   topics = generate_topics(num_topics=5)
   ```

2. Create a content brief:
   ```python
   from src.content_brief import create_brief

   brief = create_brief(topic="Future of Remote Work in HCM")
   ```

3. Generate a draft:
   ```python
   from src.draft_writer import write_draft

   draft = write_draft(brief)
   ```

4. Edit the draft:
   ```python
   from src.editor_agent import edit_draft

   edited_draft = edit_draft(draft)
   ```

5. Publish to Medium:
   ```python
   from src.publisher import publish_post

   url = publish_post(edited_draft, platform="medium", status="draft")
   ```

6. Amplify on social media:
   ```python
   from src.buffer_social_workflow import run_social_workflow

   # Run the workflow to check RSS and schedule posts
   run_social_workflow()
   ```

### Running Tests

```bash
pytest tests/
```

## Project Structure

- `src/`: Source code for the pipeline modules
- `tests/`: Unit and integration tests
- `notebooks/`: Jupyter notebooks for prototyping AI prompts
- `data/`: Topic trends and scraped data, analytics storage
- `config/`: API keys and environment variables
- `prompts/`: Default AI prompts and agent instructions

## Social Media Automation with Buffer

The pipeline includes automated social media posting via Buffer:

- Monitors RSS feeds for new Medium/Substack posts
- Generates AI-powered teaser snippets
- Schedules posts on LinkedIn and X/Twitter with configurable delays
- Logs all activities for monitoring

Configure your Buffer access token and RSS feed URL in `.env`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.