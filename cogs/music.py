from typing import NoReturn

from discord.ext import commands, tasks
from discord import FFmpegPCMAudio, PCMVolumeTransformer, VoiceChannel

from radio import what_plays_on_asiadreamradio, STATIONS


class Radio(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot        
        self.current_plays.start()
        self.now_plays = {}
        for station in STATIONS.keys():
            self.now_plays[station] = {
                'channels': [],
                'current_plays': ''
                }

    @commands.command()
    async def join(self, ctx, *, channel: VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def info(self, ctx):
        """Available radio list"""

        radios = '\n'.join(self.now_plays.keys())
        await ctx.send(f'\n{radios}')

    @commands.command()
    async def play(self, ctx, *, radio: str = None):
        """<Radio name> Plays radio"""

        if radio and radio in self.now_plays:
            params = '&'.join(['='.join(x) for x in STATIONS[radio].station_address.params.items()])
            radio_url = STATIONS[radio].station_address.url + '?' + params

            voice_id = ctx.author.voice.channel.id
            channel_id = ctx.message.channel.id
            self.now_plays[radio]['channels'].append([channel_id, voice_id])

            source = PCMVolumeTransformer(FFmpegPCMAudio(radio_url))
            ctx.voice_client.play(source, after=lambda e: print(
                f'Player error: {e}') if e else None)
            current = self.now_plays[radio]['current_plays']

            await ctx.send(f'Now playing:\n{current}')

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

        channel = ctx.message.channel.id
        for station in self.now_plays.keys():
            for i in range(len(self.now_plays[station]['channels'])):
                if self.now_plays[station]['channels'][i][0] == channel:
                    self.now_plays[station]['channels'].pop(i)
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            channel = ctx.message.channel.id
            for station in self.now_plays.keys():
                for i in range(len(self.now_plays[station]['channels'])):
                    if self.now_plays[station]['channels'][i][0] == channel:
                        self.now_plays[station]['channels'].pop(i)
        
            ctx.voice_client.stop()

    @tasks.loop(seconds=30)
    async def current_plays(self):
        for station in self.now_plays.keys():
            if len(self.now_plays[station]['channels']) > 0:
                current = what_plays_on_asiadreamradio(station)
                if current != self.now_plays[station]['current_plays']:
                    self.now_plays[station]['current_plays'] = current
                    for i, channel_id in enumerate(self.now_plays[station]['channels']):
                        ctx = self.bot.get_channel(channel_id[0])
                        voice_ctx = self.bot.get_channel(channel_id[1])
                        await ctx.send(f'Now playing:\n{current}')


async def setup(bot: commands.Bot) -> NoReturn:
    await bot.add_cog(Radio(bot))