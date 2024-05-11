from pytube import YouTube, Search
from pathlib import Path
from uuid import uuid4

from typing import cast

from re import Pattern, compile, match

yt_pattern: Pattern = compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
)


class Track:

    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def is_youtube_url(self):
        if yt_pattern.match(self.__name) is not None:
            return True

    def to_mp3(self) -> Path | None:

        if self.is_youtube_url:
            first = (
                YouTube(self.__name)
                .streams.filter(
                    only_audio=True,
                )
                .first()
            )
            if first is not None:
                return Path(
                    first.download(output_path=".saved_mp3", filename=f"{uuid4()}.mp3")
                )
            return None
        else:
            results = Search(self.__name).results
            if results is None:
                return None
            first = (
                cast(YouTube, results[0])
                .streams.filter(
                    only_audio=True,
                )
                .first()
            )

            if first is not None:
                return Path(
                    first.download(output_path=".saved_mp3", filename=f"{uuid4()}.mp3")
                )

    def __str__(self) -> str:
        return self.__name
