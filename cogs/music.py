from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands, tasks


class Radio(commands.Cog):
    """
    Support module for retranslate radio on voice chat and control him
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.__db = self.bot.connector

        self.is_listening.start()   # pylint: disable=no-member

    @commands.command()
    async def info(self, ctx):
        """Available radio list"""

        radios = "List access radio stations:\n"
        for radio in self.__db.get_radio_list():
            radios += f'{radio}\n'
        await ctx.send(radios)

    @commands.command()
    async def play(self, ctx, *, radio: str = None):
        """<Radio name> Plays radio"""

        if radio and radio in self.__db.get_radio_list():
            station_address = self.__db.get_radio_station_address(radio)
            params = '&'.join(['='.join(x)
                              for x in station_address.params.items()])
            radio_url = station_address.url + '?' + params
            source = PCMVolumeTransformer(FFmpegPCMAudio(radio_url))

            guild_id = ctx.message.guild.id
            channel_id = ctx.message.channel.id
            self.__db.set_radio_activity(guild_id, channel_id, radio)
            if self.__db.get_from_silence_group(guild_id):
                await ctx.send("Silence mod is active, if you wanna turn off, "
                               "just send '>silence off'")

            ctx.voice_client.play(source, after=lambda e: print(
                f'Player error: {e}') if e else None)

    @commands.command()
    async def volume(self, ctx, volume: int = 50):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client is not None:
            self.__db.delete_radio_activity(ctx.message.guild.id)
            await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        """Checks user who send command is on voice chat"""
        if ctx.voice_client is None:
            if ctx.author.voice is None:
                await ctx.send("You are not connected to a voice channel.")
            else:
                await ctx.author.voice.channel.connect()
        elif ctx.voice_client.is_playing():
            if ctx.author.voice:
                self.__db.delete_radio_activity(ctx.message.guild.id)
                ctx.voice_client.stop()
                if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
                    await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                await ctx.send("You must first connecting in the voice channel "
                               "before executing this command")
                raise commands.CommandInvokeError(
                    'User tried change condition without connecting in voice channel')

    @tasks.loop(seconds=30)
    async def is_listening(self):
        """
        Checking radio listeners on voice chat.
        If voice chat is empty then bot stop radio and disconnecting from voice chat
        """
        for ctx in self.bot.voice_clients:
            bot_count = 0
            for member in ctx.channel.members:
                bot_count += member.bot
            if len(ctx.channel.members) - bot_count < 1:
                ctx.stop()
                self.__db.delete_radio_activity(ctx.channel.guild.id)
                await ctx.disconnect()


async def setup(bot: commands.Bot) -> None:
    """setup func for setup_hook in main.Bot"""
    await bot.add_cog(Radio(bot))
