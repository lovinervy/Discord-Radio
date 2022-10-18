import logging

from discord import Intents
from discord.ext import commands

from db.database import Connect
from setup import add_radio, clear_activity

logging.basicConfig(level=logging.INFO, filename='logging.log', )


extensions = (
    "cogs.music",
    'cogs.notificator',
)

class Bot(commands.Bot):
    def __init__(self, db):
        self.db = db
        intents = Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or('>'),
            intents=intents
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(extension)

def main():
    from discord_token import token

    db = Connect()
    if not db.get_radio_list():
        add_radio(db)
    if db.get_radio_activity():
        clear_activity(db)
   
    bot = Bot(db)
    bot.run(token)


if __name__ == '__main__':
    main()
