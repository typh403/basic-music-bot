# Basic Music Bot

> *Note: This was one of my early Discord music bot projects, originally built to explore audio streaming mechanics and voice channel integrations.*

A lightweight, robust Discord music bot built with `discord.py` and `yt_dlp`, designed for seamless audio streaming from YouTube directly into voice channels.

## Features

- **Voice Channel Management:** Easily join (`!join`) and leave (`!leave`) voice channels.
- **High-Quality Audio Playback:** Stream tracks smoothly using `yt_dlp` and FFmpeg integration (`!play`).
- **Playback Controls:** Full control over your session with `!pause`, `!resume`, `!stop`, and `!skip`.
- **Idle Timeout Protection:** Automatically disconnects after a period of inactivity to save server resources.
- **Secure Configuration:** Utilizes environment variables (`python-dotenv`) to keep bot tokens safe and secure.

## Commands

| Command | Description |
| :--- | :--- |
| `!join` | Connects the bot to your current voice channel. |
| `!play <url>` | Streams audio from the specified YouTube link. |
| `!pause` | Pauses the current audio playback. |
| `!resume` | Resumes paused audio. |
| `!stop` | Stops the music playback. |
| `!skip` | Skips the current track. |
| `!leave` | Disconnects the bot from the voice channel. |

## Requirements

- Python 3.8+
- `discord.py`
- `yt_dlp`
- `python-dotenv`
- FFmpeg installed locally

## Setup & Installation

**1. Clone the repository:**
`git clone [https://github.com/typh403/basic-music-bot.git](https://github.com/typh403/basic-music-bot.git)`

**2. Install dependencies:**
`pip install discord.py yt_dlp python-dotenv`

**3. Create a .env file in the root directory and add your token:**
`DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN_HERE"`

**4. Run the bot:**
`python main.py`
