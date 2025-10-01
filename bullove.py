# bullove.py
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.raw import functions
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time, re

# === KONFIGURASI ===
API_ID = int("25657067")  # ganti sesuai punyamu
API_HASH = "0d1cbc0d8f3713dee1eb4d587b2c4cea"
SESSION_STRING = "ISI_SESSION_STRINGMU"

# === INIT CLIENT ===
client = Client(
    name="bullove",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

JAKARTA = ZoneInfo("Asia/Jakarta")

# === HELPER FUNGI ===
def seconds_to_dhms(sec: int):
    days, rem = divmod(sec, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return days, hours, minutes, seconds

def extract_seconds_from_exception(exc: Exception) -> int:
    # ambil nilai detik FloodWait dari atribut atau string
    for attr in ("x", "value", "seconds", "wait"):
        val = getattr(exc, attr, None)
        if isinstance(val, int) and val >= 0:
            return val
        if isinstance(val, str) and val.isdigit():
            return int(val)
    m = re.search(r"(\d+)", str(exc))
    if m:
        return int(m.group(1))
    return None

# === COMMAND PING ===
@client.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_handler(_, message):
    start = time.time()
    reply = await message.reply_text("🏓 Pinging...")
    end = time.time()
    ms = int((end - start) * 1000)
    await reply.edit(f"🏓 **PONG!**\n⏱ {ms} ms")

# === COMMAND BUAT ===
@client.on_message(filters.command("buat", prefixes=".") & filters.me)
async def buat_handler(client, message):
    teks = message.text or ""
    parts = teks.split(maxsplit=2)
    if len(parts) < 2:
        return await message.reply_text("❌ Format salah.\nContoh: `.buat g NamaGroup`")

    tipe = parts[1].lower()
    nama_raw = parts[2] if len(parts) > 2 else "Tanpa Nama"

    jumlah = 1
    nm_parts = nama_raw.split(maxsplit=1)
    if nm_parts and nm_parts[0].isdigit():
        jumlah = int(nm_parts[0])
        nama = nm_parts[1] if len(nm_parts) > 1 else "Tanpa Nama"
    else:
        nama = nama_raw

    await message.delete()
    loader = await message.reply_text(f"⏳ Sedang membuat {jumlah} item ({tipe})...")

    hasil_lines = []
    try:
        for i in range(1, jumlah + 1):
            judul = f"{nama} {i}" if jumlah > 1 else nama

            if tipe == "b":
                r = await client.invoke(
                    functions.messages.CreateChat(
                        users=[message.from_user.id],
                        title=judul
                    )
                )
                chat_id = r.chats[0].id
                link = await client.export_chat_invite_link(chat_id)
                hasil_lines.append(f"✅ Grup **{judul}** → {link}")

            elif tipe in ("g", "c"):
                r = await client.invoke(
                    functions.channels.CreateChannel(
                        title=judul,
                        about="Dibuat otomatis oleh userbot",
                        megagroup=(tipe == "g")
                    )
                )
                chat_id = r.chats[0].id
                link = await client.export_chat_invite_link(chat_id)
                kind = "Supergroup" if tipe == "g" else "Channel"
                hasil_lines.append(f"✅ {kind} **{judul}** → {link}")
            else:
                hasil_lines.append(f"❌ Tipe tidak dikenal: {tipe}")
                break

        await loader.edit("\n".join(hasil_lines), disable_web_page_preview=True)

    except Exception as exc:
        if isinstance(exc, FloodWait) or "FloodWait" in exc.__class__.__name__:
            secs = extract_seconds_from_exception(exc)
            if secs is None:
                return await loader.edit(f"❌ FloodWait.\nDetail: `{exc}`")

            days, hours, minutes, seconds = seconds_to_dhms(secs)
            now = datetime.now(JAKARTA)
            free_at = now + timedelta(seconds=secs)

            parts = []
            if days: parts.append(f"{days} hari")
            if hours: parts.append(f"{hours} jam")
            if minutes: parts.append(f"{minutes} menit")
            if seconds or not parts: parts.append(f"{seconds} detik")

            remaining_str = ", ".join(parts)
            free_at_str = free_at.strftime("%A, %d %B %Y %H:%M:%S %Z")

            await loader.edit(
                "⚠️ *Flood / Rate Limit*\n\n"
                f"⏳ Tunggu: **{remaining_str}**\n"
                f"🗓 Bebas: **{free_at_str}**",
                parse_mode="markdown"
            )
        else:
            await loader.edit(f"❌ Error: `{exc}`")

# === RUN ===
print("⚡ Bullove Userbot berjalan...")
client.run()
