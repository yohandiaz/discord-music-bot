import discord
from discord.ext.commands import Context, command, Bot, Cog
from discord import Intents
from discord import VoiceProtocol, VoiceClient
from discord import VoiceState, Member, Guild
from .guild_config import GuildConfig
from .track import Track
import os
from .music_queue import MusicQueue
from asyncio import sleep


class Server(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.__guild_relation: dict[int, GuildConfig] = {}

    def registered_guild(self, guild_id: int) -> bool:
        return guild_id in self.__guild_relation.keys()

    def register(self, guild: Guild):
        if not self.registered_guild(guild_id=guild.id):
            vc = discord.utils.get(self.bot.voice_clients, guild=guild)
            self.__guild_relation[guild.id] = GuildConfig(bot=self.bot, guild=guild)

    def get_guild_config(self, guild: Guild):
        return self.__guild_relation[guild.id]

    @staticmethod
    def current_guild(ctx: Context) -> int:
        return ctx.guild.id  # type: ignore

    @command()
    async def play(self, ctx: Context, *, track_name: str):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()  # type: ignore
        guild_config = self.get_guild_config(ctx.guild)
        guild_config.music_queue.add(Track(track_name))
        if not ctx.voice_client.is_playing():
            guild_config.play()

    @command()
    async def follow(self, ctx: Context):
        self.register(guild=ctx.guild)

        self.__guild_relation[ctx.guild.id].follow = ctx.author.id

    @Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        self.register(member.guild)

        if self.__guild_relation[member.guild.id].follow == member.id:
            print(f"saltar a canal {after.channel.name}")

            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            guild_config = self.get_guild_config(member.guild)
            guild_config.pause()
            await sleep(0.1)
            voice_client.stop()
            await voice_client.move_to(member.voice.channel)
            # guild_config.resume()
