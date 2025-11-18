# HCM Thought-Leadership Blog Pipeline

## Project Overview

This project is an AI-assisted blogging system focused on Human Capital Management (HCM), industry trends, and best practices. It provides a modular pipeline for generating blog topics, creating content briefs, drafting articles, editing for human-like quality, publishing to platforms like WordPress or Ghost, and collecting analytics on engagement.

The system is designed to support thought-leadership content creation without product promotion, leveraging AI agents to streamline the blogging process.

## Features

- **Topic Generation**: AI-powered generation of relevant HCM blog topics based on current trends.
- **Content Briefing**: Structured outlines for blog posts.
- **Draft Writing**: Automated first drafts using AI.
- **Editing**: Refinement and humanization of AI-generated text.
- **Publishing**: Automated publishing to WordPress/Ghost via API.
- **Analytics**: Collection of engagement metrics.

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
   - Fill in your API keys (OpenAI, WordPress, etc.)

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

5. Publish:
   ```python
   from src.publisher import publish_post

   publish_post(edited_draft, platform="wordpress")
   ```

### Running Tests

```bash
pytest tests/
```

## Project Structure

- `src/`: Source code for the pipeline modules
- `tests/`: Unit and integration tests
- `notebooks/`: Jupyter notebooks for prototyping AI prompts
- `data/`: Topic trends and scraped data
- `config/`: API keys and environment variables
- `prompts/`: Default AI prompts and agent instructions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.