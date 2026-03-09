import discord
from discord.ext import commands
import os
import time
import json

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

sessions = {}
points = {}

if os.path.exists("points.json"):
    with open("points.json", "r") as f:
        points = json.load(f)

def save_points():
    with open("points.json", "w") as f:
        json.dump(points, f)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != LOGIN_CHANNEL:
        return

    member = message.guild.get_member(message.author.id)

    if message.content == "تسجيل دخول":
        if not member.voice or not member.voice.channel:
            await message.reply("❌ لازم تكون داخل روم صوتي عشان تسجل دخول")
            return

        if str(member.id) in sessions:
            await message.reply("⚠️ انت مسجل دخول بالفعل")
            return

        sessions[str(member.id)] = time.time()
        await message.reply("✅ تم تسجيل دخولك")

    elif message.content == "تسجيل خروج":
        if member.voice and member.voice.channel:
            await message.reply("❌ لازم تطلع من الصوتي قبل تسجيل الخروج")
            return

        if str(member.id) not in sessions:
            await message.reply("⚠️ انت مو مسجل دخول")
            return

        start = sessions[str(member.id)]
        duration = int(time.time() - start)
        minutes = duration // 60

        del sessions[str(member.id)]

        if str(member.id) not in points:
            points[str(member.id)] = 0

        points[str(member.id)] += minutes
        save_points()

        await message.reply(f"⏱ مدة حضورك: {minutes} دقيقة\n⭐ نقاطك: {points[str(member.id)]}")

    await bot.process_commands(message)

bot.run(TOKEN)
