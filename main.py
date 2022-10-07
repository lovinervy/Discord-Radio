from discord import Intents
from discord.ext import commands
import asyncio

import logging


logging.basicConfig(level=logging.INFO, filename='logging.log')


extensions = (
    "cogs.music",
)

class Bot(commands.Bot):
    def __init__(self):
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

    bot = Bot()
    bot.run(token)


if __name__ == '__main__':
    main()
