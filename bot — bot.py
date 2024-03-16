import disnake
from disnake.ext import commands, tasks
import asyncio
from datetime import datetime
import random
import mach

bot = commands.Bot(command_prefix=".",help_command=None , intents=disnake.Intents.all(), test_guilds=[1207013223476498472])

target_channel_id = 1207169583166005288 # Замените на ID целевого канала

xp = {}

@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.idle)
    print(f'Бот {bot.user.name} готов к работе!')
    change_status.start()

@tasks.loop(seconds=10)
async def change_status():
    guild = bot.get_guild(1207013223476498472)  # Замените ID вашего сервера
    time = datetime.now().strftime('%H:%M')
    status = f'👥: {guild.member_count} | {time} МСК'
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=status))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == 1207166132285476874:  # замените на ID вашего текстового канала
        xp.setdefault(message.author.id, 0)
        xp[message.author.id] += random.randint(2, 5)  # добавляем случайное количество XP от 2 до 5 за сообщение
    await bot.process_commands(message)

@bot.event
async def update_voice_xp():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for member in guild.members:
                if member.voice and member.voice.channel:
                    xp[member.id] = xp.get(member.id, 0) + random.randint(1, 2)  # добавляем случайное количество XP от 1 до 2 за минуту в голосовом канале
        await asyncio.sleep(60)  # обновляем опыт каждые 60 секунд

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel!= after.channel and after.channel:  # если пользователь зашел в голосовой канал
        xp[member.id] = xp.get(member.id, 0) + 2
    elif before.channel!= after.channel and not after.channel:  # если пользователь вышел из голосового канала
        xp[member.id] = max(0, xp.get(member.id, 0) - 2)  # уменьшаем опыт на 2, но не ниже 0


# Нужная команда снизу!)


@bot.slash_command(description="Показывает ваш текущий опыт")
async def xp(ctx):
    user_xp = xp.get(ctx.author.id, 0)
    await ctx.send(f'Ваш текущий опыт: {user_xp} XP')

# Запустить бота
bot.run('token')