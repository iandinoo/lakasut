import asyncio
from Media import bot
from pyrogram import idle
from Media.helper.tools import *
from Media.config import LOGGER

loop = asyncio.get_event_loop_policy().get_event_loop()

async def main():
    try:
        await bot.start()
        ex = await bot.get_me()
        LOGGER("INFO").info(f"{ex.id} | 🔥 BERHASIL DIAKTIFKAN! 🔥")
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[🔥 BOT AKTIF! 🔥]")
    await idle()


LOGGER("INFO").info("Starting Bot...")
loop.run_until_complete(main())
