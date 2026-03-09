import discord
from discord.ext import commands
import os
import time
import traceback

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

sessions = {}
points = {}

@bot.event
async def on_ready():
    print(f"✅ Bot Started: {bot.user}")

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
                await message.reply("❌ لازم تكون داخل روم صوتي")
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

            if member.voice and member.voice.channel:
                await message.reply("❌ لازم تطلع من الروم الصوتي قبل تسجيل الخروج")
                return

            start = sessions[member.id]
            duration = int(time.time() - start)

            minutes = duration // 60

            del sessions[member.id]

            if member.id not in points:
                points[member.id] = 0

            points[member.id] += minutes

            await message.reply(
                f"⏱ مدة حضورك: {minutes} دقيقة\n⭐ نقاطك: {points[member.id]}"
            )

        await bot.process_commands(message)

    except Exception as e:
        print("❌ ERROR DETECTED")
        print(traceback.format_exc())

@bot.event
async def on_error(event, *args, **kwargs):
    print("⚠️ GLOBAL ERROR")
    print(traceback.format_exc())

 bot.run(TOKEN)
