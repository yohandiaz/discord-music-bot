from spotipy import Spotify

from .track import Track
from .guild_config import GuildConfig

from re import Pattern, compile


# playlist url example: https://open.spotify.com/playlist/7xLGsyNyudqvgvAuzVjPQB?si=741b83aa041d4204
playlist_pattern: Pattern = compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:open.spotify\.com))(\/(?:playlist\/)?)([\w\-]+)(\S+)?$"
)


class Playlist:

    def __init__(self, spotify: Spotify, url: str) -> None:
        self.__spotify = spotify
        self.__url = url

    @property
    def is_playlist_url(self) -> bool:  # type: ignore
        return playlist_pattern.match(self.__url) is not None

    def add_to_queue(self, tracks: list[Track], guild_config: GuildConfig):
        for t in tracks:
            guild_config.music_queue.add(t)

    def get_playlist_id(self) -> str | None:
        match = playlist_pattern.match(self.__url)
        if match is not None:
            return match.group(5)
        return None

    def get_tracks(self):
        tracks = []
        playlist = self.__spotify.playlist_items(self.get_playlist_id())
        for item in playlist["items"]:
            track = item["track"]
            tracks.append(Track(track["name"] +
                                " " +
                                track["artists"][0]["name"]))
        return tracks
