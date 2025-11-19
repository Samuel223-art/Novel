from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto
import requests
import os

# ------------------ TELEGRAM CONFIG ------------------
api_id = 21084254        # int
api_hash = "019f350964fd8f8124a0be73f5ffc8b5"  # string

# ------------------ FACEBOOK CONFIG ------------------
PAGE_ID = "884128641439706"
ACCESS_TOKEN = "EAAU81QwvDZBcBPZC5eMsBZA7pjfKhX6WbWqEHH4jsGZCZCmZBNsLyqbhzzvqIup2eohIWsCTHQ5cPJF0vDWKgTyoVQKMY4g0ni6ZAwojrULY8yoAROBfieziI5fdqii9QXdvLROTISqs8ZB3tlmoq4ZB0Tqjcv8lyMk1PjoYDzpfp780J2ZA3R8kKr9N0GU1nSVQOKzzd4piAsrgfAKDdOCLnV"

FB_GRAPH_URL = f"https://graph.facebook.com/{PAGE_ID}/photos"
# ------------------------------------------------------


client = TelegramClient("user", api_id, api_hash)


async def post_to_facebook(image_path, caption=""):
    """Upload an image with caption to Facebook Page."""
    with open(image_path, "rb") as img:
        payload = {
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
        files = {
            "source": img
        }

        response = requests.post(FB_GRAPH_URL, data=payload, files=files)
        print("FB Response:", response.json())


@client.on(events.NewMessage(chats=None))
async def handler(event):

    # Only channel messages
    if not event.is_channel:
        return

    msg = event.message

    # Only process image posts
    if not msg.media or not isinstance(msg.media, MessageMediaPhoto):
        return

    # Get caption
    caption = msg.message or ""

    # Download the image from Telegram
    image_path = await client.download_media(msg.media)

    # Upload image → Facebook
    await post_to_facebook(image_path, caption)

    # Remove temp image file
    os.remove(image_path)


print("🔥 Userbot running… Auto-sending channel images → Facebook Page")
client.start()
client.run_until_disconnected()