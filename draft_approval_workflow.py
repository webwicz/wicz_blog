#!/usr/bin/env python3
"""
Home Assistant TTS + Discord Blog Draft Approval Workflow

This script monitors a drafts folder for new blog draft files, generates TTS audio
using Home Assistant, posts to Discord for approval via reactions, and handles
the approval/rejection workflow.

Features:
- Monitors drafts folder for new .md/.txt files
- Generates TTS audio via Home Assistant API
- Posts draft content + audio to Discord approval channel
- Handles approval (✅) and rejection (❌) reactions
- Moves approved drafts to /Approved folder
- Logs all events for monitoring

Environment Variables Required:
- DISCORD_BOT_TOKEN: Discord bot token
- DISCORD_APPROVAL_CHANNEL_ID: Channel ID for approval messages
- HOME_ASSISTANT_URL: Home Assistant base URL (e.g., http://homeassistant.local:8123)
- HOME_ASSISTANT_TOKEN: Long-lived access token for Home Assistant
- DRAFTS_FOLDER: Path to drafts folder (local or Nextcloud mount)
- APPROVED_FOLDER: Path to approved drafts folder
- TTS_ENTITY_ID: Home Assistant TTS entity (e.g., tts.google_translate_say)
- TTS_LANGUAGE: Language code for TTS (e.g., en-US)
"""

import os
import asyncio
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import discord

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('draft_approval.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DraftApprovalBot(commands.Bot):
    """Discord bot for handling draft approvals via reactions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draft_messages: Dict[str, discord.Message] = {}  # draft_path -> message
        self.processed_drafts: set = set()  # Track processed drafts

    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f'Bot logged in as {self.user}')

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Handle reaction adds on draft approval messages."""
        if payload.user_id == self.user.id:  # Ignore bot's own reactions
            return

        # Check if this is a draft approval message
        message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        draft_path = None

        # Find which draft this message corresponds to
        for path, msg in self.draft_messages.items():
            if msg.id == payload.message_id:
                draft_path = path
                break

        if not draft_path:
            return

        emoji = str(payload.emoji)

        if emoji == "✅":  # Approved
            await self.handle_approval(draft_path, message)
        elif emoji == "❌":  # Rejected
            await self.handle_rejection(draft_path, message)

    async def handle_approval(self, draft_path: str, message: discord.Message):
        """Handle draft approval."""
        try:
            # Move draft to approved folder
            approved_folder = Path(os.getenv('APPROVED_FOLDER', './approved'))
            approved_folder.mkdir(exist_ok=True)

            draft_file = Path(draft_path)
            approved_path = approved_folder / draft_file.name
            draft_file.rename(approved_path)

            # Update message
            embed = message.embeds[0]
            embed.color = discord.Color.green()
            embed.add_field(name="Status", value="✅ APPROVED", inline=False)
            await message.edit(embed=embed)

            # Remove from tracking
            del self.draft_messages[draft_path]

            logger.info(f"Draft approved and moved: {draft_path} -> {approved_path}")

        except Exception as e:
            logger.error(f"Error handling approval for {draft_path}: {e}")

    async def handle_rejection(self, draft_path: str, message: discord.Message):
        """Handle draft rejection."""
        try:
            # Delete the TTS audio file (if it exists)
            audio_path = Path(draft_path).with_suffix('.mp3')
            if audio_path.exists():
                audio_path.unlink()

            # Update message
            embed = message.embeds[0]
            embed.color = discord.Color.red()
            embed.add_field(name="Status", value="❌ REJECTED", inline=False)
            await message.edit(embed=embed)

            # Log rejection
            with open('rejections.log', 'a') as f:
                f.write(f"{time.time()},{draft_path}\n")

            # Remove from tracking
            del self.draft_messages[draft_path]

            logger.info(f"Draft rejected: {draft_path}")

        except Exception as e:
            logger.error(f"Error handling rejection for {draft_path}: {e}")

class DraftFileHandler(FileSystemEventHandler):
    """File system event handler for new draft files."""

    def __init__(self, bot: DraftApprovalBot):
        self.bot = bot

    def on_created(self, event):
        """Called when a new file is created."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Check if it's a draft file
        if file_path.suffix.lower() in ['.md', '.txt'] and 'draft' in file_path.name.lower():
            logger.info(f"New draft detected: {file_path}")

            # Process the draft asynchronously
            asyncio.create_task(self.process_draft(file_path))

    async def process_draft(self, draft_path: Path):
        """Process a new draft file."""
        try:
            # Avoid processing the same draft multiple times
            if str(draft_path) in self.bot.processed_drafts:
                return

            self.bot.processed_drafts.add(str(draft_path))

            # Read draft content
            with open(draft_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Generate TTS audio
            audio_path = await generate_tts_audio(content, draft_path)

            if audio_path:
                # Send to Discord
                await send_draft_to_discord(self.bot, draft_path, content, audio_path)
            else:
                logger.error(f"Failed to generate TTS for {draft_path}")

        except Exception as e:
            logger.error(f"Error processing draft {draft_path}: {e}")

async def generate_tts_audio(content: str, draft_path: Path) -> Optional[Path]:
    """
    Generate TTS audio using Home Assistant.

    Args:
        content: Text content to convert to speech
        draft_path: Path to the draft file

    Returns:
        Path to generated audio file, or None if failed
    """
    try:
        ha_url = os.getenv('HOME_ASSISTANT_URL')
        ha_token = os.getenv('HOME_ASSISTANT_TOKEN')
        tts_entity = os.getenv('TTS_ENTITY_ID', 'tts.google_translate_say')
        language = os.getenv('TTS_LANGUAGE', 'en-US')

        if not all([ha_url, ha_token]):
            logger.error("Home Assistant URL and token not configured")
            return None

        # Prepare TTS request
        tts_url = f"{ha_url}/api/tts_get_url"
        headers = {
            'Authorization': f'Bearer {ha_token}',
            'Content-Type': 'application/json'
        }

        # Limit content length for TTS (some services have limits)
        max_length = 5000
        if len(content) > max_length:
            # Take first part and add summary note
            tts_content = content[:max_length-100] + "... [content truncated for audio]"
        else:
            tts_content = content

        data = {
            "engine": tts_entity.split('.')[1],  # Extract engine from entity_id
            "message": tts_content,
            "language": language
        }

        # Get TTS URL
        response = requests.post(tts_url, json=data, headers=headers)
        response.raise_for_status()

        audio_url = response.json().get('url')
        if not audio_url:
            logger.error("No audio URL returned from Home Assistant")
            return None

        # Download the audio file
        full_audio_url = f"{ha_url}{audio_url}"
        audio_response = requests.get(full_audio_url, headers=headers)
        audio_response.raise_for_status()

        # Save audio file
        audio_path = draft_path.with_suffix('.mp3')
        with open(audio_path, 'wb') as f:
            f.write(audio_response.content)

        logger.info(f"TTS audio generated: {audio_path}")
        return audio_path

    except Exception as e:
        logger.error(f"Error generating TTS audio: {e}")
        return None

async def send_draft_to_discord(bot: DraftApprovalBot, draft_path: Path,
                               content: str, audio_path: Path):
    """
    Send draft to Discord approval channel.

    Args:
        bot: Discord bot instance
        draft_path: Path to draft file
        content: Draft content
        audio_path: Path to audio file
    """
    try:
        channel_id = int(os.getenv('DISCORD_APPROVAL_CHANNEL_ID'))
        channel = bot.get_channel(channel_id)

        if not channel:
            logger.error(f"Could not find Discord channel {channel_id}")
            return

        # Create embed
        embed = discord.Embed(
            title=f"📝 New Blog Draft: {draft_path.name}",
            description=content[:2000] + ("..." if len(content) > 2000 else ""),  # Discord limit
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="File", value=f"`{draft_path.name}`", inline=True)
        embed.add_field(name="Size", value=f"{len(content)} characters", inline=True)
        embed.set_footer(text="React with ✅ to approve or ❌ to reject")

        # Send message with embed and audio file
        message = await channel.send(embed=embed, file=discord.File(audio_path))

        # Add reactions
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        # Track the message
        bot.draft_messages[str(draft_path)] = message

        logger.info(f"Draft sent to Discord: {draft_path}")

    except Exception as e:
        logger.error(f"Error sending draft to Discord: {e}")

async def monitor_drafts_folder():
    """Monitor the drafts folder for new files."""
    drafts_folder = Path(os.getenv('DRAFTS_FOLDER', './drafts'))

    if not drafts_folder.exists():
        logger.warning(f"Drafts folder does not exist: {drafts_folder}")
        drafts_folder.mkdir(parents=True, exist_ok=True)

    # Create bot instance
    intents = discord.Intents.default()
    intents.reactions = True
    intents.message_content = True

    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        logger.error("Discord bot token not configured")
        return

    bot = DraftApprovalBot(command_prefix='!', intents=intents)

    # Set up file monitoring
    event_handler = DraftFileHandler(bot)
    observer = Observer()
    observer.schedule(event_handler, str(drafts_folder), recursive=False)
    observer.start()

    logger.info(f"Monitoring drafts folder: {drafts_folder}")

    try:
        # Start the bot
        await bot.start(bot_token)
    except KeyboardInterrupt:
        observer.stop()
        await bot.close()
    finally:
        observer.stop()
        observer.join()

def main():
    """Main entry point."""
    logger.info("Starting Home Assistant TTS + Discord Draft Approval Workflow")

    # Validate configuration
    required_vars = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_APPROVAL_CHANNEL_ID',
        'HOME_ASSISTANT_URL',
        'HOME_ASSISTANT_TOKEN',
        'DRAFTS_FOLDER'
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(f"Missing required environment variables: {missing}")
        return

    # Run the monitoring loop
    asyncio.run(monitor_drafts_folder())

if __name__ == "__main__":
    main()