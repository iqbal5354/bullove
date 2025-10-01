import os
import glob
import importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Ambil API dan Session dari Railway Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Inisialisasi client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


# Auto load plugins dari folder "plugins"
for file in glob.glob("plugins/*.py"):
    name = os.path.splitext(os.path.basename(file))[0]
    importlib.import_module(f"plugins.{name}")


# Definisi dekorator bullove
def bullove(pattern=None):
    """Dekorator custom untuk command handler dengan prefix titik (.)"""
    def wrapper(func):
        client.add_event_handler(
            func,
            events.NewMessage(outgoing=True, pattern=pattern)  # <= outgoing True
        )
        return func
    return wrapper

async def main():
    print("⚡ Bullove Userbot berjalan...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())

