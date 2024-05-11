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

from .constants import POLLO_PUTERO


class RandomCog(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.__guild_relation: dict[int, GuildConfig] = {}

    @command()
    async def pollo_putero(self, ctx: Context, *args):

        await ctx.send(POLLO_PUTERO)
