from discord.ext import commands
import asyncio
from discord import Intents

from dotenv import load_dotenv
import os

from discord_music_bot import Server, RandomCog

from spotipy import SpotifyClientCredentials, Spotify


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", intents=Intents.all())

    load_dotenv()

    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "")

    spotify = Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    asyncio.run(bot.add_cog(Server(bot, spotify)))
    asyncio.run(bot.add_cog(RandomCog(bot)))

    bot.run(token=os.environ.get("DISCORD_TOKEN", ""))
