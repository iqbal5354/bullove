import time
from bullove import bullove

@bullove(pattern=r"^\.ping$")
async def _(e):
    start = time.time()
    xx = await e.respond("🏓 Pong...")
    end = time.time()
    ms = int((end - start) * 1000)
    await xx.edit(f"🏓 Pong!\n⏱ {ms} ms")
