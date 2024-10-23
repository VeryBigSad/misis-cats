import os

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment variables")

# Admin Chat ID
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID is not set in the environment variables")
ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)  # Convert to integer

# Channel Chat ID
CHANNEL_CHAT_ID = os.getenv("CHANNEL_CHAT_ID")
if not CHANNEL_CHAT_ID:
    raise ValueError("CHANNEL_CHAT_ID is not set in the environment variables")
CHANNEL_CHAT_ID = int(CHANNEL_CHAT_ID)  # Convert to integer

