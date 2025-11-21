#!/usr/bin/env python3
"""
Test script for Draft Approval Workflow

This script validates the configuration and tests basic functionality
without requiring live Discord/Home Assistant connections.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_configuration():
    """Test that all required environment variables are set."""
    print("🔍 Testing Configuration...")

    # Load environment
    load_dotenv(dotenv_path='config/.env')

    required_vars = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_APPROVAL_CHANNEL_ID',
        'HOME_ASSISTANT_URL',
        'HOME_ASSISTANT_TOKEN',
        'DRAFTS_FOLDER',
        'APPROVED_FOLDER'
    ]

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        elif 'your_' in value or value == '123456789012345678':
            print(f"⚠️  {var} appears to be a placeholder value")
        else:
            print(f"✅ {var} is configured")

    if missing:
        print(f"❌ Missing required variables: {missing}")
        return False

    print("✅ Configuration test passed")
    return True

def test_folders():
    """Test that required folders exist."""
    print("\n📁 Testing Folders...")

    drafts_folder = Path(os.getenv('DRAFTS_FOLDER', './drafts'))
    approved_folder = Path(os.getenv('APPROVED_FOLDER', './approved'))

    if drafts_folder.exists():
        print(f"✅ Drafts folder exists: {drafts_folder}")
    else:
        print(f"❌ Drafts folder missing: {drafts_folder}")
        return False

    if approved_folder.exists():
        print(f"✅ Approved folder exists: {approved_folder}")
    else:
        print(f"❌ Approved folder missing: {approved_folder}")
        return False

    print("✅ Folder test passed")
    return True

def test_sample_draft():
    """Test that sample draft exists and is readable."""
    print("\n📝 Testing Sample Draft...")

    drafts_folder = Path(os.getenv('DRAFTS_FOLDER', './drafts'))
    sample_draft = drafts_folder / 'sample_draft.md'

    if sample_draft.exists():
        try:
            with open(sample_draft, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Sample draft readable: {len(content)} characters")
            print(f"   Preview: {content[:100]}...")
            return True
        except Exception as e:
            print(f"❌ Error reading sample draft: {e}")
            return False
    else:
        print(f"⚠️  Sample draft not found: {sample_draft}")
        print("   (This is optional, you can create your own drafts)")
        return True

def test_imports():
    """Test that all required packages can be imported."""
    print("\n📦 Testing Imports...")

    try:
        import discord
        print(f"✅ discord.py available: {discord.__version__}")
    except ImportError:
        print("❌ discord.py not installed")
        return False

    try:
        from watchdog.observers import Observer
        print("✅ watchdog available")
    except ImportError:
        print("❌ watchdog not installed")
        return False

    try:
        import requests
        print(f"✅ requests available: {requests.__version__}")
    except ImportError:
        print("❌ requests not installed")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv available")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False

    print("✅ Import test passed")
    return True

def main():
    """Run all tests."""
    print("🚀 Draft Approval Workflow - Configuration Test")
    print("=" * 50)

    tests = [
        test_configuration,
        test_folders,
        test_sample_draft,
        test_imports
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements_draft_approval.txt")
        print("2. Configure your actual tokens in config/.env")
        print("3. Run: python draft_approval_workflow.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())