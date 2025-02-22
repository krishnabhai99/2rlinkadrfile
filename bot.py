# (©)Javpostr made by @rohit_1888

from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import time
from datetime import datetime, timedelta

from config import (
    API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, 
    FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT
)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.username = usr_bot_me.username


        if FORCE_SUB_CHANNEL2:
            try:
                expire_time = datetime.now() + timedelta(seconds=60)  # Correct: datetime object
                link = (await self.create_chat_invite_link(
                    chat_id=FORCE_SUB_CHANNEL2, 
                    creates_join_request=True, 
                    expire_date=expire_time
                )).invite_link  
                
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't export invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please double-check the FORCE_SUB_CHANNEL2 value and make sure the bot is an admin "
                    f"in the channel with 'Invite Users via Link' permission. Current value: {FORCE_SUB_CHANNEL2}"
                )
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/rohit_1888 for support")
                sys.exit()

        if FORCE_SUB_CHANNEL:
            try:
                expire_time = datetime.now() + timedelta(seconds=60)  # Correct: datetime object
                link = (await self.create_chat_invite_link(
                    chat_id=FORCE_SUB_CHANNEL, 
                    creates_join_request=True, 
                    expire_date=expire_time
                )).invite_link  
                
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't export invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(
                    f"Please double-check the FORCE_SUB_CHANNEL value and make sure the bot is an admin "
                    f"in the channel with 'Invite Users via Link' permission. Current value: {FORCE_SUB_CHANNEL}"
                )
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/rohit_1888 for support")
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make sure the bot is an admin in the DB Channel and double-check the CHANNEL_ID value. "
                f"Current value: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/rohit_1888 for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..! Made by @rohit_1888")   

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info("Bot is now running. Thanks to @rohit_1888")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())