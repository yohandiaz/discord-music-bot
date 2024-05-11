from .track import Track

from threading import Thread
from discord import VoiceClient


class MusicQueue:

    def __init__(self) -> None:
        self.__music_queue: list[Track] = []

    def add(self, track: Track):

        self.__music_queue.append(track)

    def next(self) -> Track | None:
        if len(self.__music_queue) > 0:
            return self.__music_queue[0]
        else:
            return None

    def pop(self) -> Track | None:
        if len(self.__music_queue) > 0:
            return self.__music_queue.pop(0)
        else:
            return None
