import discord
from discord.ext import commands
import time
import json
import os

TOKEN = "PUT_YOUR_TOKEN_HERE"
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

sessions = {}
points = {}

# تحميل النقاط
if os.path.exists("points.json"):
    with open("points.json", "r") as f:
        points = json.load(f)

def save_points():
    with open("points.json", "w") as f:
        json.dump(points, f)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != LOGIN_CHANNEL:
        return

    member = message.author
    guild_member = message.guild.get_member(member.id)

    # تسجيل دخول
    if message.content == "تسجيل دخول":

        if not guild_member.voice or not guild_member.voice.channel:
            await message.reply("❌ لازم تكون داخل روم صوتي عشان تسجل دخول")
            return

        if str(member.id) in sessions:
            await message.reply("⚠️ انت مسجل دخول بالفعل")
            return

        sessions[str(member.id)] = time.time()

        await message.reply("✅ تم تسجيل دخولك وبدأ حساب الوقت")

    # تسجيل خروج
    if message.content == "تسجيل خروج":

        if guild_member.voice and guild_member.voice.channel:
            await message.reply("❌ لازم تطلع من الروم الصوتي قبل تسجيل الخروج")
            return

        if str(member.id) not in sessions:
            await message.reply("⚠️ انت مو مسجل دخول")
            return

        start = sessions[str(member.id)]
        spent = int(time.time() - start)

        minutes = spent // 60

        del sessions[str(member.id)]

        if str(member.id) not in points:
            points[str(member.id)] = 0

        points[str(member.id)] += minutes

        save_points()

        await message.reply(
            f"⏱ مدة حضورك: {minutes} دقيقة\n⭐ نقاطك الحالية: {points[str(member.id)]}"
        )

    await bot.process_commands(message)

bot.run(TOKEN)
