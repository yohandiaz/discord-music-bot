from pytube import YouTube
from pathlib import Path


class Track:

    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def is_youtube_url(self):

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
                    first.download(output_path=".saved_mp3", filename="test.mp3")
                )
            return None
