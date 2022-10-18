from typing import List

from discord.ext import commands, tasks

from db.database import Connect, radioActivity
from my_types.radio import StationScoreboardAddress
from radio import what_plays_on_asiadreamradio


class Radio_Notify(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.__db = self.bot.db
        self.send_notification.start()
    
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
                await ctx.send("If you don't want to be notified what play on radio, just send '>silence on'")

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
        if last_data == current_data or None == current_data:
            return False
        return True

    def __radio_listens(self, activity: List[radioActivity]) -> List[str]:
        radios = []
        if activity == None:
            return radios
        for channel in activity:
            radios.append(channel.radio)
        return radios
    
    def __update_last_scoreboard_data(self, radio_name: str, data: str):
        if self.__db.get_last_scoreboard(radio_name):
            self.__db.update_last_scoreboard(radio_name, data)
        else:
            self.__db.set_last_scoreboard(radio_name, data)

    async def __update_current_scoreboard_data(self, radio_name: str, scoreboard: StationScoreboardAddress):
        
        data = await what_plays_on_asiadreamradio(scoreboard)
        last_data = self.__db.get_current_scoreboard(radio_name)
        if data is None:
            pass
        elif last_data is None:
            self.__db.set_current_scoreboard(radio_name, data.to_str())
        elif last_data != data.to_str():
            self.__db.update_current_scoreboard(radio_name, data.to_str())

    @tasks.loop(seconds=30)
    async def send_notification(self):
        active_channels: List[radioActivity] = self.__db.get_radio_activity()
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
    await bot.add_cog(Radio_Notify(bot))
