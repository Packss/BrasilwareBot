# bot.py

# vai se fuder jakez

import discord
import os
import random
import asyncio
import jishaku

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = int(os.environ['DISCORD_GUILD'])

bot = commands.Bot(command_prefix='bw.')

bot.load_extension('jishaku')


@bot.command(name='teste', help="Testa se o bot está ativo")
async def teste(ctx):
    await ctx.send('Testado!')


@bot.command(name='ping', help="Pong!")
async def ping(ctx):
    await ctx.send(f'Ping: {round(bot.latency, 3)*1000}ms\n{ctx.author.mention}')


@bot.event
async def is_owner(user: discord.User):
    for role in user.roles:
        if str(role) == "SU":
            print(f"O usuario {user} pertence ao SU, executando comando")
            return True


bumplock = False
bumplist = []
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    lista = message.content.split(' ')[:2]
    check = (
        lista[0] in ('!d', '!disboard'),
        lista[1] == 'bump'
    )
    if all(check):
        global bumplock, bumplist

        if bumplock == True:
            await message.channel.send(
                f"{message.author.mention} o servidor teve um bump a menos de 2 horas, por favor espere.\nPorém vou te mencionar quando o proximo bump estiver disponivel"
                )
            bumplist.append(message.author.mention)

        else:
            await message.channel.send(
                "Irei te lembrar daqui 2 horas!"
                )
            bumplock = True
            await asyncio.sleep(7200)
            bumplock = False
            await message.channel.send(
                f"{message.author.mention} hora de dar bump!"
                )
            for member in bumplist:
                await message.channel.send(
                    f"{member} você tentou dar um bump, agora é a hora"
                )
            bumplist.clear()

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name} seja bem vindo ao Brasilware!\n'
        f'Sinta-se livre para conversar e pedir ajuda, e não se esqueça de ler as <#729796356067033088>.'
    )


bot.run(TOKEN)
