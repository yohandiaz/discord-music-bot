import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to keep track of music queues for each guild
queues = {}

def check_queue(ctx):
    # This function should be called when a song ends
    if ctx.guild.id in queues and queues[ctx.guild.id]:
        # Get the next track from the queue
        next_track = queues[ctx.guild.id].pop(0)
        play_next_track(ctx, next_track)
    else:
        # No more songs in the queue, possibly disconnect or send a message
        # await ctx.send("Queue is empty. Leaving the voice channel.")
        pass

def play_next_track(ctx, filename):
    # This function is responsible for playing the next track in the queue
    source = discord.FFmpegPCMAudio(filename)
    ctx.voice_client.play(source, after=lambda e: [os.remove(filename) if os.path.exists(filename) else None, check_queue(ctx)])

@bot.command(name='play', help='Searches and plays the first result from YouTube')
async def play(ctx, *, search: str):
    voice_client = ctx.voice_client
    if not voice_client:
        if ctx.author.voice:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("You are not connected to a voice channel.")

    if voice_client.is_playing() or voice_client.is_paused():
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(search)  # Store search query instead of filename
        await ctx.send(f"Added to queue: {search}")
    else:
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0'
        }

        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=True)
            video = info['entries'][0]
            filename = ydl.prepare_filename(video)
            filename = filename.replace(".webm", ".mp3")

        play_next_track(ctx, filename)

@bot.command(name='skip', help='Skips the current track')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped the current track.")
        check_queue(ctx)
    else:
        await ctx.send("No music is currently playing.")

@bot.command(name='pause', help='Pauses the music')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Music paused.")

@bot.command(name='resume', help='Resumes the music')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Music resumed.")

@bot.command(name='stop', help='Stops the music')
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        queues[ctx.guild.id] = []  # Clear the queue
        await ctx.send("Music stopped and queue cleared.")

# Get token from env variable
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
