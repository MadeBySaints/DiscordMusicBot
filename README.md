# DiscordMusicBot
A music bot for discord written in python.


## Discord Music Bot
This Discord bot allows users to play music from YouTube directly into a voice channel. It uses the discord.py library for interaction with Discord and yt-dlp for downloading and playing music.

## Features
Connects to a Discord server and joins a voice channel.

Plays music from YouTube based on a search query.

Queues songs if one is already playing.

Skips to the next song in the queue with a command.

Uses asynchronous programming to handle music playback and bot commands without blocking.

## Requirements
Python 3.6 or higher

discord.py library

yt-dlp library

FFmpeg installed and accessible in your system's PATH

## Setup
Clone the Repository:

git clone [https://github.com/MadeBySaints/discord-music-bot.git](https://github.com/MadeBySaints/DiscordMusicBot.git)

cd discord-music-bot

## Install Dependencies:
pip install -U discord.py yt-dlp

## Configure the Bot:
Inside the config.json file, set your Discord channels, and bot token.

## Run the Bot:
python main.py or just run the included startbot.bat

## Usage
Use /play <song name or YouTube URL> to play a song or add it to the queue.

Use /skip to skip the current song and play the next in the queue.

## Implementation Details
The bot uses discord.ext.commands.Bot for creating and managing commands.

Music downloading is handled by yt-dlp, with postprocessing to convert videos to MP3.

Asynchronous programming patterns are used throughout, with tasks that potentially block the main thread (like downloading music) being run in an executor.

## Troubleshooting
If the bot does not play music or join the voice channel:

Ensure your bot token and voice channel ID are correctly set in config.json.

Verify that FFmpeg is correctly installed and accessible in your system's PATH.

Check for any error messages in the console and address them accordingly.


## Contributing
Contributions are welcome! If you have a feature request, bug report, or pull request, please open an issue or submit a pull request on GitHub.
