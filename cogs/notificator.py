from typing import List

from discord.ext import commands, tasks

from db.database import RadioActivity
from my_types.radio import StationScoreboardAddress
from radio import what_plays_on_asiadreamradio


class RadioNotify(commands.Cog):
    """
    Support module for checking info updates on radio station and
    sending notification to radio listeners
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.__db = self.bot.connector
        self.send_notification.start()  # pylint: disable=no-member

    @commands.command()
    async def silence(self, ctx, *, status: str = None):
        """Radio notifiter to turned on or off, send as '>silence on/off'"""

        guild_id = ctx.message.guild.id

        match status:
            case "on":
                self.__add_in_silence_group(guild_id)
                await ctx.send("Silence mod on")
            case "off":
                self.__remove_from_silence_group(guild_id)
                await ctx.send("Silence mod off")
            case _:
                await ctx.send("If you don't want to be notified what play on radio, "
                               "just send '>silence on'")

    def __add_in_silence_group(self, guild_id: int):
        if not self.__is_in_silence_group(guild_id):
            self.__db.add_in_silence_group(guild_id)

    def __remove_from_silence_group(self, guild_id: int):
        if self.__is_in_silence_group(guild_id):
            self.__db.delete_from_silence_group(guild_id)

    def __is_in_silence_group(self, guild_id: int) -> bool:
        if self.__db.get_from_silence_group(guild_id):
            return True
        return False

    def __is_new_radio_data(self, radio_name: str) -> bool:
        last_data = self.__db.get_last_scoreboard(radio_name)
        current_data = self.__db.get_current_scoreboard(radio_name)
        if last_data == current_data or current_data is None:
            return False
        return True

    def __radio_listens(self, activity: List[RadioActivity]) -> List[str]:
        radios = []
        if activity is None:
            return radios
        for channel in activity:
            radios.append(channel.radio)
        return radios

    def __update_last_scoreboard_data(self, radio_name: str, data: str):
        if self.__db.get_last_scoreboard(radio_name):
            self.__db.update_last_scoreboard(radio_name, data)
        else:
            self.__db.set_last_scoreboard(radio_name, data)

    async def __update_current_scoreboard_data(self, radio_name: str,
                                               scoreboard: StationScoreboardAddress):

        data = await what_plays_on_asiadreamradio(scoreboard)
        last_data = self.__db.get_current_scoreboard(radio_name)
        if data is None:
            pass
        elif last_data is None:
            self.__db.set_current_scoreboard(radio_name, repr(data))
        elif last_data != repr(data):
            self.__db.update_current_scoreboard(radio_name, repr(data))

    @tasks.loop(seconds=30)
    async def send_notification(self):
        """Send info about song play in dicord channel. Check every 30 seconds"""
        active_channels: List[RadioActivity] = self.__db.get_radio_activity()
        radio_list = self.__radio_listens(active_channels)
        for radio in radio_list:
            scoreboard = self.__db.get_radio_scoreboard_address(radio)
            await self.__update_current_scoreboard_data(radio, scoreboard)
            if self.__is_new_radio_data(radio):
                data = self.__db.get_current_scoreboard(radio)
                self.__update_last_scoreboard_data(radio, data)
                for channel in active_channels:
                    if channel.radio == radio and \
                            not self.__is_in_silence_group(channel.guild_id):
                        ctx = self.bot.get_channel(channel.channel_id)
                        if ctx is not None:
                            message = f'Radio: {radio}\n{data}'
                            await ctx.send(message)
                        else:
                            self.__db.delete_radio_activity(channel.guild_id)


async def setup(bot: commands.Bot) -> None:
    """setup func for setup_hook in main.Bot"""
    await bot.add_cog(RadioNotify(bot))
