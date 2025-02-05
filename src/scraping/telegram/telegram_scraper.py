from telethon import TelegramClient
import os
import json

# Telegram API credentials (replace with actual API ID and Hash)
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')

if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in environment variables")

# Channels to scrape
CHANNELS = [
    'https://t.me/DoctorsET',
    'https://t.me/lobelia4cosmetics',
    'https://t.me/yetenaweg',
    'https://t.me/EAHCI',
    'https://t.me/CheMed123'
]

# Directory to store scraped data
RAW_DATA_DIR = '../../data/raw'
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Initialize Telegram Client
client = TelegramClient('besu', API_ID, API_HASH)

async def scrape_channel(channel):
    messages = []
    try:
        async for message in client.iter_messages(channel, limit=100):
            messages.append({
                'id': message.id,
                'date': str(message.date),
                'text': message.text,
                'sender_id': message.sender_id
            })

        # Save messages to JSON file
        with open(os.path.join(RAW_DATA_DIR, f'{channel.replace("https://t.me/", "")}.json'), 'w') as f:
            json.dump(messages, f, indent=4)

        print(f"Scraped {len(messages)} messages from {channel}")
    except Exception as e:
        print(f"Error scraping {channel}: {e}")

async def main():
    await client.start(PHONE_NUMBER)
    for channel in CHANNELS:
        await scrape_channel(channel)
    await client.disconnect()