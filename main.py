import discord
from discord.ext import commands
from datetime import datetime, timezone
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

voice_join_times = {}

# ايدي روم التكست
LOG_CHANNEL_ID = 1473015218211651706


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):

    channel = bot.get_channel(LOG_CHANNEL_ID)

    # دخول فويس
    if before.channel is None and after.channel is not None:

        join_time = datetime.now(timezone.utc)
        voice_join_times[member.id] = join_time

        if channel:
            await channel.send(
                f"🟢 **{member.name}** دخل روم الصوت **{after.channel.name}** "
                f"الساعة {join_time.strftime('%H:%M')}"
            )

    # خروج فويس
    if before.channel is not None and after.channel is None:

        if member.id in voice_join_times:

            join_time = voice_join_times[member.id]
            duration = datetime.now(timezone.utc) - join_time

            minutes, seconds = divmod(int(duration.total_seconds()), 60)

            if channel:
                await channel.send(
                    f"🔴 **{member.name}** خرج من الصوت بعد "
                    f"{minutes} دقيقة و {seconds} ثانية"
                )

            del voice_join_times[member.id]


TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
