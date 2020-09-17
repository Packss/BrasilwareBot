# bot.py
import discord
import os
import random
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

bot = commands.Bot(command_prefix='bw.')


@bot.command(name='teste', help="Testa se o bot está ativo")
async def nine_nine(ctx):
    await ctx.send('Testado!')


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.content.startswith('!d bump'):
        await message.channel.send("Irei te lembrar daqui 2 horas!")
        await asyncio.sleep(7200)
        await message.channel.send(f"{message.author.mention} hora de dar bump!")

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Membros do server:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name} seja bem vindo ao Brasilware!\n Sinta-se livre para conversar e pedir ajuda, e não se esqueça de ler as regras.'
    )


bot.run(TOKEN)
