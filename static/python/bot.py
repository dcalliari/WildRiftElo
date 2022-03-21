import os
import static.python.mod as mod

from dotenv import load_dotenv
from os.path import join
from twitchio.ext import commands
from twitchio.client import Client

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
CHANNELS = mod.get_channel()
BOT_NICK = os.environ.get('BOT_NICK')


bot = commands.Bot(
    prefix=PREFIX,
    token=TOKEN,
    initial_channels=CHANNELS,
    heartbeat=30.0
)

client = Client(
    token=TOKEN,
    heartbeat=30.0
)


@bot.event()
async def event_ready():
    print(f"{BOT_NICK} ta online!")


@bot.event()
async def event_message(message):
    try:
        autor = message.author.name
    except AttributeError:
        return
    if autor.lower() == BOT_NICK.lower():
        return
    CHANNEL = message.channel.name
    msg = message.content
    time = message.timestamp.strftime('%H:%M:%S')
    print(f'#{CHANNEL} {time} {autor}: {msg}')


@bot.command(name="update")
async def update(ctx):
    if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
        os.system("git pull")
        print("Atualizando e reiniciando...")
        os.system("python3 bot.py")
        exit()


@bot.command(name='tutorial', aliases=['tuto'])
@mod.cooldown
async def command_tutorial(ctx):
    if ctx.channel.name.lower() == BOT_NICK.lower():
        await ctx.channel.send('/me Como adicionar o bot e configurar em seu canal: https://imgur.com/a/zl1T2CY')
    else:
        await ctx.channel.send(f'/me Envie !tutorial no chat do {BOT_NICK}')


@bot.command(name='entrar', aliases=['join'])
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if AUTHOR == '1bode':
        try:
            AUTHOR = ctx.message.content.split()[1]
        except IndexError:
            pass
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHANNELS:
            await ctx.channel.send(f'/me Bot JÁ ESTÁ no canal {AUTHOR}')
        else:
            CHANNELS.append(f'#{AUTHOR}')
            mod.update_channel(CHANNELS)
            mod.file_check(AUTHOR)
            await bot.join_channels(CHANNELS)
            await ctx.channel.send(f'/me Bot ENTROU no canal {AUTHOR}')


@bot.command(name='sair', aliases=['leave'])
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if AUTHOR == '1bode':
        try:
            AUTHOR = ctx.message.content.split()[1]
        except IndexError:
            pass
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHANNELS:
            CHANNELS.remove(f'#{AUTHOR}')
            mod.update_channel(CHANNELS)
            await ctx.channel.send(F'/me Bot SAIU do canal {AUTHOR}')
        else:
            await ctx.channel.send(F'/me Bot NÃO ESTÁ no canal {AUTHOR}')


@bot.command(name='elos')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    try:
        elo = mod.get_elo('', CHANNEL)
        div = mod.get_div('', CHANNEL)
        conta = mod.get_conta('', CHANNEL)
        elo1 = mod.get_elo('1', CHANNEL)
        div1 = mod.get_div('1', CHANNEL)
        conta1 = mod.get_conta('1', CHANNEL)
        elo2 = mod.get_elo('2', CHANNEL)
        div2 = mod.get_div('2', CHANNEL)
        conta2 = mod.get_conta('2', CHANNEL)
        elo3 = mod.get_elo('3', CHANNEL)
        div3 = mod.get_div('3', CHANNEL)
        conta3 = mod.get_conta('3', CHANNEL)
        await ctx.channel.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
    except KeyError:
        try:
            elo = mod.get_elo('', CHANNEL)
            div = mod.get_div('', CHANNEL)
            conta = mod.get_conta('', CHANNEL)
            elo1 = mod.get_elo('1', CHANNEL)
            div1 = mod.get_div('1', CHANNEL)
            conta1 = mod.get_conta('1', CHANNEL)
            elo2 = mod.get_elo('2', CHANNEL)
            div2 = mod.get_div('2', CHANNEL)
            conta2 = mod.get_conta('2', CHANNEL)
            await ctx.channel.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
        except KeyError:
            try:
                elo = mod.get_elo('', CHANNEL)
                div = mod.get_div('', CHANNEL)
                conta = mod.get_conta('', CHANNEL)
                elo1 = mod.get_elo('1', CHANNEL)
                div1 = mod.get_div('1', CHANNEL)
                conta1 = mod.get_conta('1', CHANNEL)
                await ctx.channel.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1}')
            except KeyError:
                try:
                    elo1 = mod.get_elo('1', CHANNEL)
                    div1 = mod.get_div('1', CHANNEL)
                    conta1 = mod.get_conta('1', CHANNEL)
                    elo2 = mod.get_elo('2', CHANNEL)
                    div2 = mod.get_div('2', CHANNEL)
                    conta2 = mod.get_conta('2', CHANNEL)
                    elo3 = mod.get_elo('3', CHANNEL)
                    div3 = mod.get_div('3', CHANNEL)
                    conta3 = mod.get_conta('3', CHANNEL)
                    await ctx.channel.send(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
                except KeyError:
                    try:
                        elo1 = mod.get_elo('1', CHANNEL)
                        div1 = mod.get_div('1', CHANNEL)
                        conta1 = mod.get_conta('1', CHANNEL)
                        elo2 = mod.get_elo('2', CHANNEL)
                        div2 = mod.get_div('2', CHANNEL)
                        conta2 = mod.get_conta('2', CHANNEL)
                        await ctx.channel.send(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
                    except KeyError:
                        await ctx.channel.send('/me Você precisa configurar pelo menos duas contas.')


@bot.command(name='conta', aliases=['conta1', 'conta2', 'conta3', 'smurf', 'elosmurf'])
async def command_conta(ctx):
    CHANNEL = ctx.channel.name.lower()
    ac = ctx.message.content.split(' ', 1)[0][-1]
    ac = '' if ac == 'a' else ac
    ac = 1 if ac == 'f' else ac
    if ctx.message.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            conta = f'Conta{ac}'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.channel.send('/me Valor inválido')
                return
            mod.update_value(f'conta{ac}', conta, CHANNEL)
            await ctx.channel.send(f'/me Nome da conta{ac} atualizado para: {conta}')


@bot.command(name='elo', aliases=['elo1', 'elo2', 'elo3'])
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    ac = ctx.message.content.split(' ', 1)[0][-1]
    ac = '' if ac == 'o' else ac
    if ctx.message.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.channel.send('/me Valor inválido')
                return
            mod.update_value(f'elo{ac}', elo, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
            await ctx.channel.send(f'/me Elo de "{conta}" atualizado para {elo}')

    else:
        elo = mod.get_elo(ac, CHANNEL)
        div = mod.get_div(ac, CHANNEL)
        pdl = mod.get_pdl(ac, CHANNEL)
        drt = mod.get_drt(ac, CHANNEL)
        conta = mod.get_conta(ac, CHANNEL)
        await ctx.channel.send(f'/me {conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='div', aliases=['div1', 'div2', 'div3'])
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    ac = ctx.message.content.split(' ', 1)[0][-1]
    ac = '' if ac == 'v' else ac
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.message.content.split(' ', 1)[1:][0]
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            await ctx.channel.send('/me Valor inválido')
            return
        mod.update_value(f'div{ac}', div, CHANNEL)
        conta = mod.get_conta(ac, CHANNEL)
        await ctx.channel.send(f'/me Divisão de "{conta}" atualizada para {div}')


@bot.command(name='pdl', aliases=['pdl1', 'pdl2', 'pdl3'])
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    ac = ctx.message.content.split(' ', 1)[0][-1]
    ac = '' if ac == 'l' else ac
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.message.content.split(' ', 1)[1:][0]
        try:
            pdl = mod.get_pdl(ac, CHANNEL)
        except KeyError:
            pdl = 0
        if command_string.startswith('+'):
            val = command_string.replace('+', '').strip()
            try:
                pdl += int(val)
            except ValueError:
                await ctx.channel.send('/me Valor inválido')
                return
            mod.update_value(f'pdl{ac}', pdl, CHANNEL)
            elo = mod.get_elo(ac, CHANNEL)
            div = mod.get_div(ac, CHANNEL)
            drt = mod.get_drt(ac, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
        elif command_string.startswith('-'):
            val = command_string.replace('-', '').strip()
            try:
                pdl -= int(val)
            except ValueError:
                await ctx.channel.send('/me Valor inválido')
                return
            mod.update_value(f'pdl{ac}', pdl, CHANNEL)
            elo = mod.get_elo(ac, CHANNEL)
            div = mod.get_div(ac, CHANNEL)
            drt = mod.get_drt(ac, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
        else:
            try:
                pdl = int(command_string)
            except ValueError:
                await ctx.channel.send('/me Valor inválido')
                return
            mod.update_value(f'pdl{ac}', pdl, CHANNEL)
            elo = mod.get_elo(ac, CHANNEL)
            div = mod.get_div(ac, CHANNEL)
            drt = mod.get_drt(ac, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
        await ctx.channel.send(f'/me {conta}: {elo} {div} ({pdl} {drt})')


if __name__ == "__main__":
    bot.run()
