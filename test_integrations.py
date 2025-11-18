"""
Test Script for x.ai and Nextcloud Integration

This script tests the x.ai API connection and Nextcloud file upload.
"""

import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(dotenv_path='config/.env')

from src.topic_generator import generate_topics
from src.scheduler import upload_to_nextcloud

def test_xai_api():
    """Test x.ai API by generating research topics."""
    print("Testing x.ai API...")
    xai_key = os.getenv('XAI_API_KEY')
    if not xai_key:
        print("❌ XAI_API_KEY not found in environment variables. Please check your .env file.")
        return False

    try:
        topics = generate_topics(num_topics=3, mode='research')
        print(f"✅ x.ai API working! Generated {len(topics)} topics:")
        for topic in topics:
            print(f"  - {topic}")
        return True
    except Exception as e:
        print(f"❌ x.ai API test failed: {e}")
        return False

def test_nextcloud_upload():
    """Test Nextcloud upload by creating and uploading a test file."""
    print("Testing Nextcloud upload...")
    nc_url = os.getenv('NEXTCLOUD_URL')
    nc_user = os.getenv('NEXTCLOUD_USERNAME')
    nc_pass = os.getenv('NEXTCLOUD_PASSWORD')

    if not all([nc_url, nc_user, nc_pass]):
        print("❌ Nextcloud credentials not found in environment variables. Please check your .env file.")
        return False

    try:
        # Create a test file
        from datetime import datetime
        test_content = f"Test file created on {datetime.now().isoformat()}"
        test_file = os.path.join(os.path.dirname(__file__), 'data', 'test_upload.txt')
        with open(test_file, 'w') as f:
            f.write(test_content)

        # Upload to Nextcloud
        remote_path = 'Blog/Test/test_upload.txt'
        upload_to_nextcloud(test_file, remote_path)

        print(f"✅ Nextcloud upload successful! File uploaded to: {remote_path}")
        return True
    except Exception as e:
        print(f"❌ Nextcloud upload test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting integration tests...\n")

    xai_ok = test_xai_api()
    print()
    nextcloud_ok = test_nextcloud_upload()

    print("\n" + "="*50)
    if xai_ok and nextcloud_ok:
        print("🎉 All tests passed! Integrations are working.")
    else:
        print("⚠️  Some tests failed. Check your credentials and try again.")
    print("="*50)

if __name__ == "__main__":
    main()