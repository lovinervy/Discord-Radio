from typing import NoReturn

from discord.ext import commands, tasks
from radio import STATIONS


class Radio_Notify(commands.Cog):
    def __init__(self, bot: commands.Bot) -> NoReturn:
        self.bot = bot

        self.radio_notify = {}      # {station <type: str> : [ channel_id ] <type: List[int]>
        self.__init_stations()

    @commands.Cog.listener()
    async def on_message(self, message) -> NoReturn:
        print(message.content)
        prefix = self.bot.command_prefix
        if message.content.startswith(prefix):
            cmd = message.content.split(' ')
            if cmd[0] == f'{prefix}play':
                self.play(message.channel.id, message.content)
            elif cmd[0] == f'{prefix}stop':
                self.stop(message.channel.id, message.content)

    def play(self, channel_id: int, message_content: str):
        station = message_content.split('>play ')[1]
        if station in self.radio_notify:
            self.radio_notify[station] = channel_id
    
    def stop(self, channel_id: int):
        for station in self.radio_notify.keys():
            for i in self.radio_notify[station]:
                if self.radio_notify[station][i] == channel_id:
                    self.radio_notify[station].pop(i)

    def __init_stations(self):
        for station in STATIONS.keys():
            self.radio_notify[station] = []


async def setup(bot: commands.Bot) -> NoReturn:
    await bot.add_cog(Radio_Notify(bot))
