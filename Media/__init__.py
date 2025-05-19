import sys
import asyncio
import os
import pytz

from pyromod import listen
from pyrogram import Client
from pyrogram.types import *
from pyrogram import __version__

from Media.config import *

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "Media/modules"},
            workers=4,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.id = usr_bot_me.id
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.id}\n└ Username: @{self.id}"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Berhenti."
            )
            sys.exit()
            
bot = Bot()
