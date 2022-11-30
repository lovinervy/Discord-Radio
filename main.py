import logging

from discord import Intents
from discord.ext import commands

from db.engine import SQLite
from db.database import Connect
from setup import add_radio, clear_activity
from discord_token import TOKEN

logging.basicConfig(level=logging.INFO, filename='logging.log', )


extensions = (
    "cogs.music",
    'cogs.notificator',
)


class Bot(commands.Bot):
    """
    Main Bot class for run support modules,
    set database connector and connect do discord server
    """

    def __init__(self, connector: Connect):
        self.connector = connector
        intents = Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or('>'),
            intents=intents
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(extension)


def main():
    """main function for run application"""

    engine = SQLite()
    connector = Connect(engine)
    if not connector.get_radio_list():
        add_radio(connector)
    if connector.get_radio_activity():
        clear_activity(connector)

    bot = Bot(connector)
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
