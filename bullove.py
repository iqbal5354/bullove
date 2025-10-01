import os
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID", "123456"))  # ganti di Railway ENV
API_HASH = os.getenv("API_HASH", "your_api_hash")
SESSION_STRING = os.getenv("SESSION_STRING", None)  # opsional
BOT_TOKEN = os.getenv("BOT_TOKEN", None)  # kalau pakai bot

if SESSION_STRING:
    bullove = Client(
        "bullove",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )
elif BOT_TOKEN:
    bullove = Client(
        "bullove",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
else:
    raise Exception("Harus set SESSION_STRING atau BOT_TOKEN di Railway ENV!")

@bullove.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(client, message):
    await message.edit("🏓 Pong!")

print("⚡ Bullove Userbot berjalan...")
bullove.run()
