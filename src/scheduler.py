"""
Scheduler Script for Tri-Weekly Blog Workflow

This script runs the blog pipeline on a tri-weekly cadence (Mon, Wed, Fri).
- Weekly (Monday): Research HCM topics
- Tri-weekly (Mon, Wed, Fri): Generate topic report for review
- Integrates with Nextcloud for file management
"""

import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from src.topic_generator import generate_topics

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(dotenv_path='../config/.env')

def is_tri_weekly_day():
    """Check if today is Monday, Wednesday, or Friday."""
    today = datetime.now().weekday()  # 0=Monday, 2=Wednesday, 4=Friday
    return today in [0, 2, 4]

def is_monday():
    """Check if today is Monday."""
    return datetime.now().weekday() == 0

def upload_to_nextcloud(file_path, remote_path):
    """
    Upload a file to Nextcloud via WebDAV.

    Args:
        file_path (str): Local file path
        remote_path (str): Remote path in Nextcloud
    """
    try:
        nextcloud_url = os.getenv('NEXTCLOUD_URL')  # e.g., https://your-nextcloud.com/remote.php/dav/files/username/
        username = os.getenv('NEXTCLOUD_USERNAME')
        password = os.getenv('NEXTCLOUD_PASSWORD')

        if not all([nextcloud_url, username, password]):
            logger.warning("Nextcloud credentials not set, skipping upload.")
            return

        with open(file_path, 'rb') as f:
            response = requests.put(
                f"{nextcloud_url}{remote_path}",
                data=f,
                auth=(username, password)
            )
        response.raise_for_status()
        logger.info(f"Uploaded {file_path} to Nextcloud: {remote_path}")
    except Exception as e:
        logger.error(f"Error uploading to Nextcloud: {e}")

def run_weekly_workflow():
    """Run weekly research on Monday."""
    logger.info("Running weekly HCM topic research...")
    try:
        topics = generate_topics(num_topics=10, mode='research')
        # Save research topics for later use
        research_file = os.path.join(os.path.dirname(__file__), '..', 'data', f"research_topics_{datetime.now().strftime('%Y-%m-%d')}.txt")
        with open(research_file, 'w') as f:
            f.write('\n'.join(topics))
        logger.info(f"Saved research topics to {research_file}")
        upload_to_nextcloud(research_file, f"Blog/Research/research_topics_{datetime.now().strftime('%Y-%m-%d')}.txt")
    except Exception as e:
        logger.error(f"Weekly workflow failed: {e}")

def run_tri_weekly_workflow():
    """Run tri-weekly report generation."""
    logger.info("Running tri-weekly topic report...")
    try:
        report = generate_topics(num_topics=5, mode='report')
        # Save report
        report_file = os.path.join(os.path.dirname(__file__), '..', 'data', f"topic_report_{datetime.now().strftime('%Y-%m-%d')}.md")
        with open(report_file, 'w') as f:
            f.write(report)
        logger.info(f"Saved topic report to {report_file}")
        upload_to_nextcloud(report_file, f"Blog/Reports/topic_report_{datetime.now().strftime('%Y-%m-%d')}.md")
    except Exception as e:
        logger.error(f"Tri-weekly workflow failed: {e}")

def main():
    """Main scheduler function."""
    today = datetime.now()

    if is_monday():
        run_weekly_workflow()

    if is_tri_weekly_day():
        run_tri_weekly_workflow()

    logger.info("Workflow completed for today.")

if __name__ == "__main__":
    main()