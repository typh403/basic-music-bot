import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from the .env file for secure token handling
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Use yt_dlp for robust and updated YouTube extraction, with fallback support
try:
  import yt_dlp
except ImportError:
  import youtube_dl as yt_dlp

# Configure bot intents required for message content and voice state management
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Initialize bot instance with command prefix '!'
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  """Executed when the bot successfully connects and goes online."""
  print(f"{bot.user} is successfully connected and active!")


@bot.command(name="join")
async def join(ctx):
  """Connects the bot to the author's current voice channel."""
  if ctx.author.voice is None:
    await ctx.send("You need to be in a voice channel first!")
    return

  channel = ctx.author.voice.channel
  vc = ctx.voice_client

  # Disconnect from any existing connection before joining a new channel
  if vc and vc.is_connected():
    await vc.disconnect()

  await channel.connect()
  await ctx.send(f"Connected to **{channel.name}**.")


@bot.command(name="play")
async def play(ctx, url: str):
  """Streams audio from a given YouTube URL into the voice channel."""
  vc = ctx.voice_client

  if not vc or not vc.is_connected():
    await ctx.send("You must invite the bot to a voice channel first (`!join`)!")
    return

  # yt_dlp extraction configurations
  ydl_opts = {
      "format": "bestaudio/best",
      "quiet": True,
      "noplaylist": True,
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    audio_url = info["url"]

  # Stop current playback if something is already playing
  if vc.is_playing():
    vc.stop()

  # Play the audio stream using FFmpeg executable path and reconnection options
  vc.play(
      discord.FFmpegPCMAudio(
          audio_url,
          executable=(
              "C:\\Users\\26seh\\Desktop\\ffmpeg-8.1-essentials_build\\ffmpeg-8.1-essentials_build\\bin\\ffmpeg.exe"
          ),
          before_options=(
              "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
          ),
          options="-vn",
      ),
      after=lambda e: asyncio.run_coroutine_threadsafe(
          idle_check(ctx), bot.loop
      ),
  )

  await ctx.send(f"Now playing: **{info['title']}**")


async def idle_check(ctx):
  """Automatically disconnects the bot if it remains inactive/idle for a set period."""
  await asyncio.sleep(300)  # Wait for 5 minutes of inactivity

  vc = ctx.voice_client

  if vc and not vc.is_playing():
    await ctx.send(
        "No music has been played for a while. Are you still listening?"
    )
    await asyncio.sleep(60)  # Wait an additional 1 minute
    if vc and not vc.is_playing():
      await ctx.send("Disconnecting due to inactivity.")
      await vc.disconnect()


@bot.command(name="stop")
async def stop(ctx):
  """Stops the current audio playback."""
  vc = ctx.voice_client

  if vc and vc.is_playing():
    vc.stop()
    await ctx.send("Playback stopped.")
  else:
    await ctx.send("There is no active audio playing right now.")


@bot.command(name="pause")
async def pause(ctx):
  """Pauses the current audio stream."""
  vc = ctx.voice_client

  if vc and vc.is_playing():
    vc.pause()
    await ctx.send("Playback paused.")
  else:
    await ctx.send("No active playback to pause.")


@bot.command(name="resume")
async def resume(ctx):
  """Resumes paused audio playback."""
  vc = ctx.voice_client

  if vc and vc.is_paused():
    vc.resume()
    await ctx.send("Resuming playback.")
  else:
    await ctx.send("The audio is not paused.")


@bot.command(name="skip")
async def skip(ctx):
  """Skips the current track by stopping the active playback stream."""
  vc = ctx.voice_client

  if vc and vc.is_playing():
    vc.stop()
    await ctx.send("Skipping to the next track.")
  else:
    await ctx.send("There is no track to skip.")


@bot.command(name="leave")
async def leave(ctx):
  """Disconnects the bot from the voice channel."""
  vc = ctx.voice_client
  if vc and vc.is_connected():
    await vc.disconnect()
    await ctx.send("Disconnected from the voice channel.")
  else:
    await ctx.send("I am not connected to any voice channel.")


# Run the bot securely utilizing the environment token
bot.run(TOKEN)