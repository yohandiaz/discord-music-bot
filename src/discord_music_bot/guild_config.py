from dataclasses import dataclass
from .music_queue import MusicQueue
from discord import VoiceClient
import discord
import os
from datetime import datetime, timedelta
from discord.ext.commands import Context, command, Bot, Cog
from discord import Guild


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
                    after=lambda e: [
                        source.cleanup(),
                        os.remove(filename) if self.pause_time is None else None,
                        self.music_queue.pop() if self.pause_time is None else None,
                        print(self.pause_time),
                        (
                            self.play(
                                int((self.pause_time - self.start_time).total_seconds())
                            )
                            if self.pause_time is not None
                            and self.start_time is not None
                            else self.play()
                        ),
                    ],
                )

    @property
    def voice_client(self) -> VoiceClient:
        vc = discord.utils.get(self.bot.voice_clients, guild=self.guild)
        return vc

    def pause(self):
        self.pause_time = datetime.now()
