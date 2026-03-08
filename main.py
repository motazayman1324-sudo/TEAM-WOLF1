import discord
from discord.ext import commands
from datetime import datetime, timezone
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

voice_join_times = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):

    # دخول روم صوتي
    if before.channel is None and after.channel is not None:

        join_time = datetime.now(timezone.utc)
        voice_join_times[member.id] = join_time

        try:
            await member.send(
                f"🎙️ Welcome {member.name}! "
                f"You joined {after.channel.name} at {join_time.strftime('%H:%M')}"
            )
        except:
            print(f"Couldn't DM {member.name}")

    # خروج من روم صوتي
    if before.channel is not None and after.channel is None:

        if member.id in voice_join_times:

            join_time = voice_join_times[member.id]
            duration = datetime.now(timezone.utc) - join_time

            minutes, seconds = divmod(int(duration.total_seconds()), 60)

            try:
                await member.send(
                    f"👋 {member.name}, you stayed in voice for {minutes}m {seconds}s"
                )
            except:
                print(f"Couldn't DM {member.name}")

            del voice_join_times[member.id]


# قراءة التوكن من الاستضافة
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
