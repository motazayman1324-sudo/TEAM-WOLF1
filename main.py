import discord
from discord.ext import commands
import os
import time

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

sessions = {}
points = {}

@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != LOGIN_CHANNEL:
        return

    member = message.guild.get_member(message.author.id)

    if message.content == "تسجيل دخول":

        if member.voice is None or member.voice.channel is None:
            await message.reply("❌ لازم تكون داخل روم صوتي")
            return

        if member.id in sessions:
            await message.reply("⚠️ انت مسجل دخول بالفعل")
            return

        sessions[member.id] = time.time()
        await message.reply("✅ تم تسجيل دخولك")

    elif message.content == "تسجيل خروج":

        if member.id not in sessions:
            await message.reply("❌ انت مو مسجل دخول")
            return

        if member.voice and member.voice.channel:
            await message.reply("❌ اطلع من الصوتي قبل تسجيل الخروج")
            return

        start = sessions[member.id]
        duration = int(time.time() - start)
        minutes = duration // 60

        del sessions[member.id]

        if member.id not in points:
            points[member.id] = 0

        points[member.id] += minutes

        await message.reply(f"⏱ جلست {minutes} دقيقة\n⭐ نقاطك: {points[member.id]}")

    await bot.process_commands(message)

 bot.run(TOKEN)
