import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import json
import asyncio
import traceback

TOKEN = os.getenv("TOKEN")
LOGIN_CHANNEL = 1473015218211651706

# رتب التصفير
ALLOWED_ROLES = [1473015044643094643, 1473015048443269160]

# رتب عرض النقاط
ALLOWED_VIEW_ROLES = [
    1473783225535955207,
    1480382273760137426,
    1473015044643094643,
    1473015048443269160
]

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
    return f"⏳ {h:02}:{m:02}:{s:02}"

def has_permission(member):
    return any(role.id in ALLOWED_ROLES for role in member.roles)

def has_view_permission(member):
    return any(role.id in ALLOWED_VIEW_ROLES for role in member.roles)

@bot.event
async def on_ready():
    print(f"🤖 Bot Online: {bot.user}")
    await bot.tree.sync()

# ======================
# Slash Commands
# ======================

@bot.tree.command(name="نقاط", description="عرض نقاط عضو")
@app_commands.describe(member="اختر العضو")
async def points_command(interaction: discord.Interaction, member: discord.Member):

    if not has_view_permission(interaction.user):
        await interaction.response.send_message("❌ | ليس لديك صلاحية.", ephemeral=True)
        return

    user_points = points.get(str(member.id), 0)

    await interaction.response.send_message(
        f"📊 | نقاط {member.mention}: **{user_points}**"
    )

@bot.tree.command(name="صفر", description="تصفير نقاط عضو")
@app_commands.describe(member="اختر العضو")
async def reset_user_points(interaction: discord.Interaction, member: discord.Member):

    if not has_permission(interaction.user):
        await interaction.response.send_message("❌ | ليس لديك صلاحية.", ephemeral=True)
        return

    points[str(member.id)] = 0
    save_points()

    await interaction.response.send_message(f"🧹 | تم تصفير نقاط {member.mention}")

@bot.tree.command(name="تصفير", description="تصفير جميع النقاط")
async def reset_all_points(interaction: discord.Interaction):

    if not has_permission(interaction.user):
        await interaction.response.send_message("❌ | ليس لديك صلاحية.", ephemeral=True)
        return

    points.clear()
    save_points()

    await interaction.response.send_message("🧹 | تم تصفير جميع النقاط")

# ======================
# نظام الحضور
# ======================

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
                await message.reply("❌ | لازم تكون داخل روم صوتي.")
                return

            if member.id in sessions:
                await message.reply("⚠️ | انت مسجل بالفعل.")
                return

            sessions[member.id] = time.time()
            await message.reply("🟢 | تم تسجيل دخولك.")

        elif message.content == "تسجيل خروج":

            if member.id not in sessions:
                await message.reply("❌ | انت غير مسجل.")
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

            await message.reply(
                f"⏳ الوقت: {format_time(duration)}\n"
                f"⭐ النقاط: {earned_points}\n"
                f"🏆 مجموعك: {points[str(member.id)]}"
            )

        await bot.process_commands(message)

    except Exception:
        print(traceback.format_exc())

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if member.id not in sessions:
            return

        if before.channel and not after.channel:

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

            leave_timers[member.id] = asyncio.create_task(leave_timer())

        if after.channel:
            if member.id in leave_timers:
                leave_timers[member.id].cancel()
                del leave_timers[member.id]

    except Exception:
        print(traceback.format_exc())

bot.run(TOKEN)
