import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Ambil API dan Session dari Railway Environment Variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Inisialisasi client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Definisi dekorator bullove
def bullove(**kwargs):
    """Dekorator custom untuk command handler."""
    def wrapper(func):
        client.add_event_handler(func, events.NewMessage(**kwargs))
        return func
    return wrapper

async def main():
    print("⚡ Bullove Userbot berjalan...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
