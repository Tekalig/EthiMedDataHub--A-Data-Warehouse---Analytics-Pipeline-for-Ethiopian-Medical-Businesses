from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Telegram API credentials (reuse from the main scraper) from the .env file
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')

# Channels to scrape images from
CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/CheMed123'
]

# Directory to store scraped images
IMAGES_DIR = '../../data/raw/images'
os.makedirs(IMAGES_DIR, exist_ok=True)

# Initialize Telegram Client
client = TelegramClient('session_name', API_ID, API_HASH)

async def download_images(channel):
    try:
        async for message in client.iter_messages(channel, limit=100):
            if message.photo:
                image_path = os.path.join(IMAGES_DIR, f'{channel.replace("https://t.me/", "")}_{message.id}.jpg')
                await client.download_media(message, image_path)
                print(f"Downloaded image from {channel}: {image_path}")
    except Exception as e:
        print(f"Error downloading images from {channel}: {e}")

async def main():
    await client.start(PHONE_NUMBER)
    for channel in CHANNELS:
        await download_images(channel)
    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
