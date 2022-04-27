import os
from pyrogram import Client

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

FORCE_SUB = os.environ.get("FORCE_SUB", None)           

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
       await super().start()
       me = await self.get_me()
       self.username = me.username
       print("Bot Started")
        
    async def stop(self, *args):
      await super().stop()
      print("Bot Stopped")
        
bot = Bot()
bot.run()
