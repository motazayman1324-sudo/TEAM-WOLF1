import discord
from discord.ext import commands
import os
import time
import json
import traceback

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

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
    print(f"Bot Online: {bot.user}")

@bot.event
async def on_message(message):

    try:

        if message.author.bot:
            return

        if message.channel.id != LOGIN_CHANNEL:
            return

        member = message.guild.get_member(message.author.id)

        # تسجيل دخول
        if message.content == "تسجيل دخول":

            if not member.voice or not member.voice.channel:
                await message.reply("❌ لازم تكون داخل روم صوتي لتسجيل الدخول")
                return

            if member.id in sessions:
                await message.reply("⚠️ انت مسجل دخول بالفعل")
                return

            sessions[member.id] = time.time()

            await message.reply("✅ تم تسجيل دخولك وبدأ حساب الوقت")

        # تسجيل خروج
        elif message.content == "تسجيل خروج":

            if member.id not in sessions:
                await message.reply("❌ انت مو مسجل دخول")
                return

            start = sessions[member.id]
            duration = int(time.time() - start)

            hours = duration / 3600
            earned_points = int(hours * 30)

            del sessions[member.id]

            if str(member.id) not in points:
                points[str(member.id)] = 0

            points[str(member.id)] += earned_points

            save_points()

            minutes = duration // 60

            await message.reply(
                f"⏱ مدة حضورك: {minutes} دقيقة\n⭐ النقاط المكتسبة: {earned_points}\n🏆 مجموع نقاطك: {points[str(member.id)]}"
            )

        await bot.process_commands(message)

    except Exception:
        print("ERROR")
        print(traceback.format_exc())

bot.run(TOKEN)
