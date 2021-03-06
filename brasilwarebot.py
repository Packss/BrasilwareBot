# bot.py

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
    ping= round(bot.latency, 3)*1000
    await ctx.send(f"{ctx.author.mention} meu ping é de {ping}ms!")


@bot.command(name='roll', help="Rola um dado, caso nenhum seja especificado o d20 é rolado")
async def roll(ctx, dado="d20"):
    possiveis = [3, 4, 6, 8, 10, 20, 32]
    if int(dado[1:]) in possiveis:
        resultado = random.randint(1, int(dado[1:]))
        await ctx.send(f"Você rolou {resultado}!")
    else:
        lista = ""
        for x in possiveis:
            lista = lista+f"d{x} "
        await ctx.send(f"Valor {dado} não suportado.\nOs valores suportados são: {lista}")
        

@bot.event
async def is_owner(user: discord.User):
    for role in user.roles:
        if str(role) == "SU":
            print(f"O usuario {user} pertence ao SU, executando comando")
            return True


bot.bumplock = False
bot.bumplist = []
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    lista = message.content.split(' ')[:2]
    if len(lista) == 1: return

    check = (
        lista[0] in ('!d', '!disboard'),
        lista[1] == 'bump',
        message.channel.id == 751589697192591501
    )
    
    if all(check):
        if bot.bumplock == True:
            if message.author.mention not in bot.bumplist:
                await message.channel.send(
                    f"{message.author.mention} o servidor teve um bump a menos de 2 horas, por favor espere.\nPorém vou te mencionar quando o proximo bump estiver disponivel"
                    )
                bot.bumplist.append(message.author.mention)
            else:
                await message.channel.send(
                    f"{message.author.mention} Você ja tentou dar bump, pare imediatamente."
                    )

        else:
            await message.channel.send(
                "Irei te lembrar daqui 2 horas!"
                )
            bot.bumplist.append(message.author.mention)

            bot.bumplock = True
            await asyncio.sleep(7200)
            bot.bumplock = False

            await message.channel.send(
                f"{message.author.mention} hora de dar bump!"
                )
            for member in bot.bumplist[1:]:
                await message.channel.send(
                    f"{member} você tentou dar um bump, agora é a hora"
                )
            bot.bumplist.clear()


@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD)
    print(
        f'{bot.user} está conectado a essa guilda:\n'
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
