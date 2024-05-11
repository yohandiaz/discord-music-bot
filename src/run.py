from discord.ext import commands
import asyncio
from discord import Intents

from dotenv import load_dotenv
import os

from discord_music_bot import Server, RandomCog


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", intents=Intents.all())

    asyncio.run(bot.add_cog(Server(bot)))
    asyncio.run(bot.add_cog(RandomCog(bot)))

    bot.run(token=os.environ.get("DISCORD_TOKEN", ""))
