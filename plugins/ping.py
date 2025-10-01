import time
from bullove import bullove

@bullove(pattern=r"\.ping")
async def _(e):
    print("✅ Event .ping terdeteksi")  # debug log ke Railway
    await e.respond("🏓 Pong!")
