from discord.ext.commands import Context, command, Bot, Cog

from discord import VoiceState, Member, Guild
from .guild_config import GuildConfig
from .track import Track
from .playlist import Playlist

from discord import VoiceChannel

from spotipy import Spotify


class Server(Cog):

    def __init__(self, bot: Bot, spotify: Spotify) -> None:
        self.bot = bot
        self.spotify = spotify
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

        if args is None:
            await ctx.send("Please provide a track name or spotify playlist!")
            return

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()  # type: ignore

        guild_config = self.get_guild_config(ctx.guild)

        playlist = Playlist(self.spotify, args[0])
        if playlist.is_playlist_url:
            tracks = playlist.get_tracks()
            playlist.add_to_queue(tracks, guild_config)
            await ctx.send("Playlist added to queue!")
        else:
            guild_config.music_queue.add(Track(args[0]))
            await ctx.send("Track added to queue!")

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

    @command()
    async def stats(self, ctx: Context):
        if ctx.guild is None:
            await ctx.send("This command can only be runned from a server")
            return
        self.register(guild=ctx.guild)
        guild_config = self.get_guild_config(ctx.guild)
        await ctx.send("Stats:\n" + guild_config.get_stats())

    @Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState | None, after: VoiceState | None
    ):
        self.register(member.guild)

        guild_config = self.get_guild_config(member.guild)

        # if the bot joins a channel
        if (
            self.bot.user is not None
            and self.bot.user.id == member.id
            and after is not None
            and after.channel is not None
            and after.channel.id == guild_config.voice_client.channel.id
        ):
            for i_member in guild_config.members:
                if (
                    i_member.id != self.bot.user.id
                    and i_member.voice is not None
                    and i_member.voice.channel is not None
                    and after.channel.id == i_member.voice.channel.id
                ):
                    guild_config.member_start_listen(i_member)

        # if someone joins on the lobby bot
        if (
            self.bot.user is not None
            and self.bot.user.id != member.id
            and after is not None
            and after.channel is not None
            and after.channel.id == guild_config.voice_client.channel.id
        ):
            guild_config.member_start_listen(member)

        if (
            self.bot.user is not None
            and self.bot.user.id != member.id
            and before is not None
            and before.channel is not None
            and before.channel.id == guild_config.voice_client.channel.id
        ):
            guild_config.member_stop_listen(member)

        if after is not None:
            if guild_config.follow == member.id:

                if after.channel is None:
                    print("error 1")
                    return
                guild_config = self.get_guild_config(member.guild)

                if isinstance(after.channel, VoiceChannel):

                    await guild_config.move_to_channel(after.channel)
