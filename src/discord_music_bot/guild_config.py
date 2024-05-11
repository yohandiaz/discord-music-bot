from dataclasses import dataclass
from .music_queue import MusicQueue
from discord import VoiceClient
import discord
import os
from datetime import datetime, timedelta
from discord.ext.commands import Context, command, Bot, Cog
from discord import Guild
from typing import cast
from pathlib import Path
from discord import VoiceChannel
from asyncio import sleep


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{seconds:02}"


@dataclass(kw_only=True)
class GuildConfig:

    follow: int | None = None
    bot: Bot
    guild: Guild
    music_queue: MusicQueue = MusicQueue()
    start_time: datetime | None = None
    pause_time: datetime | None = None

    playing: bool = False

    def play(self, start_time: int = 0):
        seconds_to_hms(start_time)
        self.start_time = datetime.now() - timedelta(seconds=start_time)
        self.pause_time = None
        next = self.music_queue.next()
        if next is not None:
            filename = next.to_mp3()
            if filename is not None:
                source = discord.FFmpegPCMAudio(
                    str(filename), before_options=f"-ss {seconds_to_hms(start_time)}"
                )
                self.voice_client.play(  # type: ignore
                    source,
                    after=lambda e: self.end_track(source=source, filename=filename),
                )

    def end_track(self, source: discord.FFmpegPCMAudio, filename: Path):

        source.cleanup()
        if self.pause_time is None:
            os.remove(filename)
            self.music_queue.pop()

        if self.pause_time is not None and self.start_time is not None:
            self.play(int((self.pause_time - self.start_time).total_seconds()))
        else:
            self.play()

    @property
    def voice_client(self) -> VoiceClient:
        vc = discord.utils.get(self.bot.voice_clients, guild=self.guild)
        return cast(VoiceClient, vc)

    def pause(self):
        self.pause_time = datetime.now()
        self.voice_client.stop()

    def skip(self):

        self.voice_client.stop()

    @property
    def is_paused(self) -> bool:
        return self.pause_time is not None

    async def move_to_channel(self, channel: VoiceChannel):
        vc = self.voice_client
        if vc != channel.id:
            self.pause()
            await sleep(0.3)
            vc.stop()
            await self.voice_client.move_to(channel)
