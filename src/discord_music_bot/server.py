from discord.ext.commands import Context, command, Bot, Cog

from discord import VoiceState, Member, Guild
from .guild_config import GuildConfig
from .track import Track

from discord import VoiceChannel


class Server(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.__guild_relation: dict[int, GuildConfig] = {}

    def registered_guild(self, guild_id: int) -> bool:
        return guild_id in self.__guild_relation.keys()

    def register(self, guild: Guild):
        if not self.registered_guild(guild_id=guild.id):
            self.__guild_relation[guild.id] = GuildConfig(bot=self.bot, guild=guild)

    def get_guild_config(self, guild: Guild):
        return self.__guild_relation[guild.id]

    @command()
    async def p(self, ctx: Context, *args):
        await self.play(ctx, *args)

    @command()
    async def play(self, ctx: Context, *args):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return

        track_name = "_".join(args)
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()  # type: ignore
        guild_config = self.get_guild_config(ctx.guild)
        guild_config.music_queue.add(Track(track_name))
        if not guild_config.voice_client.is_playing():
            guild_config.play()

    @command()
    async def queue(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        self.register(guild=ctx.guild)

        guild_config = self.get_guild_config(ctx.guild)

        await ctx.send(str(guild_config.music_queue))

    @command()
    async def skip(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        self.register(guild=ctx.guild)

        guild_config = self.get_guild_config(ctx.guild)
        guild_config.skip()

    @command()
    async def unfollow(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        self.register(guild=ctx.guild)

        self.__guild_relation[ctx.guild.id].follow = None

    @command()
    async def follow(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        self.register(guild=ctx.guild)

        self.__guild_relation[ctx.guild.id].follow = ctx.author.id

    def get_voice_channels(self, guild: Guild) -> list[VoiceChannel]:

        return guild.voice_channels

    @command()
    async def move(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        config = self.get_guild_config(ctx.guild)
        if config.follow is not None:
            await ctx.send(f"This bot is following {config.follow} and can't be moved")

        self.get_voice_channels

    @Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState | None
    ):
        self.register(member.guild)

        if after is None:
            return
        if self.__guild_relation[member.guild.id].follow == member.id:

            if after.channel is None:
                print("error 1")
                return
            guild_config = self.get_guild_config(member.guild)

            if isinstance(after.channel, VoiceChannel):

                await guild_config.move_to_channel(after.channel)
