import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
import json

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

bot_token = config["bot_token"]
voice_channel_id = int(config["voice_channel_id"])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents) # Change the command identifier here

queue = []  # Initialize queue to store song requests

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    channel = bot.get_channel(voice_channel_id)
    if not discord.utils.get(bot.voice_clients, guild=channel.guild):
        await channel.connect()

async def download_song(search: str):
    # Define the synchronous part of downloading a song as a separate function
    def sync_download(search):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'songs/%(title)s.%(ext)s',
            'quiet': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            # Check if the song already exists before downloading
            file_name = f'songs/{info["title"]}.mp3'
            if not os.path.isfile(file_name):
                ydl.download([info['webpage_url']])
            else:
                print(f"File {file_name} already exists. Skipping download.")
            return info

    # Run the synchronous function in an executor
    loop = asyncio.get_running_loop()
    info = await loop.run_in_executor(None, sync_download, search)
    return info

@bot.command()
async def play(ctx, *, search: str):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        await ctx.send("The bot is not connected to a voice channel.")
        return

    info = await download_song(search)
    title = info['title']
    file_name = f'songs/{title}.mp3'

    if voice_client.is_playing() or queue:
        queue.append((ctx, file_name, info))
        await ctx.send(f"Song **{title}** queued!")
    else:
        await play_song(ctx, voice_client, info, file_name)

async def play_song(ctx, voice_client, info, file_name):
    embed = discord.Embed(title=info['title'], url=info['webpage_url'], color=discord.Color.blue())
    embed.set_author(name="Now Playing")
    if 'thumbnail' in info:
        embed.set_thumbnail(url=info['thumbnail'])
    await ctx.send(embed=embed)
    
    voice_client.play(discord.FFmpegPCMAudio(file_name), after=lambda e: asyncio.run_coroutine_threadsafe(on_song_end(e, ctx), bot.loop))

async def on_song_end(error, ctx):
    if error:
        print(f'Player error: {error}')
    await asyncio.sleep(1)  # Wait a moment for the next song
    if queue:
        _, file_name, info = queue.pop(0)
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await play_song(ctx, voice_client, info, file_name)

@bot.command()
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped! Playing next in queue..." if queue else "Skipped! No more songs in the queue.")

bot.run(bot_token)
