# Home Assistant TTS + Discord Blog Draft Approval Workflow

This workflow provides a fully automated, mobile-friendly system for managing blog draft approvals using Home Assistant Text-to-Speech (TTS) and Discord reactions.

## Features

- 🔍 **Automatic Draft Detection**: Monitors a drafts folder for new `.md` or `.txt` files
- 🔊 **TTS Audio Generation**: Uses Home Assistant to create audio versions of drafts
- 💬 **Discord Integration**: Posts drafts with audio to a dedicated approval channel
- 👍👎 **Reaction-Based Approval**: Uses Discord reactions (✅ approve, ❌ reject)
- 📁 **File Management**: Automatically moves approved drafts and cleans up rejected ones
- 📝 **Comprehensive Logging**: Tracks all events for monitoring and debugging

## Prerequisites

### 1. Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Invite the bot to your server with appropriate permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Add Reactions

### 2. Home Assistant Setup
1. Install a TTS integration (Google Translate TTS is recommended)
2. Create a long-lived access token:
   - Go to your Home Assistant profile
   - Scroll to "Long-lived access tokens"
   - Create a new token
3. Note your Home Assistant URL (e.g., `http://homeassistant.local:8123`)

### 3. Folder Setup
Create the following directories:
- `drafts/` - Place new draft files here
- `approved/` - Approved drafts will be moved here automatically

## Installation

1. Install dependencies:
```bash
pip install -r requirements_draft_approval.txt
```

2. Configure environment variables in `config/.env`:
```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_APPROVAL_CHANNEL_ID=123456789012345678

# Home Assistant Configuration
HOME_ASSISTANT_URL=http://your-ha-url:8123
HOME_ASSISTANT_TOKEN=your_long_lived_token_here
TTS_ENTITY_ID=tts.google_translate_say
TTS_LANGUAGE=en-US

# Folder Configuration
DRAFTS_FOLDER=./drafts
APPROVED_FOLDER=./approved
```

## Usage

### Starting the Workflow

Run the draft approval bot:
```bash
python draft_approval_workflow.py
```

The bot will:
1. Start monitoring the drafts folder
2. Log into Discord
3. Wait for new draft files

### Creating Drafts

1. Write your blog draft as a `.md` or `.txt` file
2. Save it in the `drafts/` folder
3. The system will automatically:
   - Generate TTS audio using Home Assistant
   - Post to Discord with text content and audio file
   - Add ✅ and ❌ reaction options

### Approval Process

**On Mobile/Desktop Discord:**
1. Open the approval channel
2. Listen to the audio or read the text
3. React with:
   - ✅ **Approve**: Draft moves to `approved/` folder
   - ❌ **Reject**: Audio file deleted, rejection logged

### Monitoring

Check the logs:
- `draft_approval.log` - All workflow events
- `rejections.log` - Timestamped rejection records

## Configuration Options

### TTS Settings
- `TTS_ENTITY_ID`: Home Assistant TTS entity (default: `tts.google_translate_say`)
- `TTS_LANGUAGE`: Language code (default: `en-US`)

### Folder Paths
- `DRAFTS_FOLDER`: Where to monitor for new drafts (default: `./drafts`)
- `APPROVED_FOLDER`: Where approved drafts are moved (default: `./approved`)

### Discord Settings
- `DISCORD_APPROVAL_CHANNEL_ID`: Channel ID for approval messages
- `DISCORD_BOT_TOKEN`: Your Discord bot token

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to reactions**
   - Ensure bot has "Add Reactions" and "Read Message History" permissions
   - Check that the channel ID is correct

2. **TTS generation fails**
   - Verify Home Assistant URL and token
   - Check that TTS integration is installed and working
   - Ensure TTS entity ID is correct

3. **File monitoring not working**
   - Check that drafts folder exists and is writable
   - Ensure no other processes are locking the files

### Logs

All events are logged to `draft_approval.log`. Check this file for detailed error messages and workflow status.

## Architecture

The system is built with a modular design:

- `DraftApprovalBot`: Discord bot handling reactions and approvals
- `DraftFileHandler`: File system monitoring for new drafts
- `generate_tts_audio()`: Home Assistant TTS integration
- `send_draft_to_discord()`: Discord message creation and file upload
- `handle_approval()` / `handle_rejection()`: Workflow completion logic

## Security Notes

- Store tokens securely and never commit to version control
- Use HTTPS for Home Assistant if exposed to internet
- Regularly rotate Discord bot tokens and Home Assistant access tokens
- Monitor logs for unauthorized access attempts

## Future Enhancements

- Multiple approval channels for different content types
- Custom TTS voices and languages per draft
- Integration with content management systems
- Automated publishing after approval
- Analytics dashboard for approval metrics