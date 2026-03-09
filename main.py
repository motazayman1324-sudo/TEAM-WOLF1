import discord
from discord.ext import commands
import os
import time
import json
import asyncio
import traceback

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

sessions = {}
points = {}
leave_timers = {}

if os.path.exists("points.json"):
    with open("points.json","r") as f:
        points = json.load(f)

def save_points():
    with open("points.json","w") as f:
        json.dump(points,f)

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    parts = []
    if h > 0:
        parts.append(f"{h} ساعة")
    if m > 0:
        parts.append(f"{m} دقيقة")
    if s > 0:
        parts.append(f"{s} ثانية")

    return " و ".join(parts)

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

        if message.content == "تسجيل دخول":

            if not member.voice or not member.voice.channel:
                await message.reply("❌ لازم تكون داخل روم صوتي")
                return

            if member.id in sessions:
                await message.reply("⚠️ انت مسجل دخول بالفعل")
                return

            sessions[member.id] = time.time()

            await message.reply("✅ تم تسجيل دخولك وبدأ حساب الوقت")

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

            time_text = format_time(duration)

            await message.reply(
                f"📋 مدة حضورك: {time_text}\n⭐ النقاط المكتسبة: {earned_points}\n🏆 مجموع نقاطك: {points[str(member.id)]}"
            )

        await bot.process_commands(message)

    except Exception:
        print(traceback.format_exc())

@bot.event
async def on_voice_state_update(member, before, after):

    try:

        if member.id not in sessions:
            return

        # خرج من الصوتي
        if before.channel and not after.channel:

            try:
                await member.send("تم رصد خروجك من الروم الصوتي. لديك 5 دقايق للعودة قبل إلغاء تسجيل الدخول.")
            except:
                pass

            async def leave_timer():

                await asyncio.sleep(300)

                if member.id in sessions and (not member.voice or not member.voice.channel):

                    start = sessions[member.id]
                    duration = int(time.time() - start)

                    hours = duration / 3600
                    earned_points = int(hours * 30)

                    del sessions[member.id]

                    if str(member.id) not in points:
                        points[str(member.id)] = 0

                    points[str(member.id)] += earned_points
                    save_points()

                    try:
                        await member.send("⏰ انتهت المهلة (5 دقايق)، وتم إلغاء تسجيل دخولك تلقائيًا.")
                    except:
                        pass

            leave_timers[member.id] = asyncio.create_task(leave_timer())

        # رجع للصوتي
        if after.channel:

            if member.id in leave_timers:
                leave_timers[member.id].cancel()
                del leave_timers[member.id]

                try:
                    await member.send("✅ تم رصد عودتك للروم الصوتي. تم إلغاء المهلة.")
                except:
                    pass

    except Exception:
        print(traceback.format_exc())

bot.run(TOKEN)
