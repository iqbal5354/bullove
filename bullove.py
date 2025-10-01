import asyncio
from pyrogram import Client, filters
import os

# Ambil variabel dari environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bullove = Client(
    "bullove",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Command ping
@bullove.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(_, message):
    await message.reply_text("Pong!")

print("⚡ Bullove Userbot berjalan...")
bullove.run()
