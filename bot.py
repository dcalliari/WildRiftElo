import io
import os
import json
import unidecode

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def get_channel():
    JSON_FILE = str(os.path.dirname(
        os.path.realpath(__file__))) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        global CHAN
        CHAN = data['CHANNEL']
    return CHAN


def update_channel(value):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channels.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['CHANNEL'] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=get_channel()
)

client = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)


@bot.event
async def event_ready():
    print(f"{BOT_NICK} ta online!")


@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BOT_NICK.lower():
        return
    await bot.handle_commands(ctx)


@bot.command(name='tutorial')
async def command_tutorial(ctx):
    await ctx.send_me('Como adicionar o bot e configurar em seu canal: https://imgur.com/gallery/zl1T2CY')


@bot.command(name='entrar')
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHAN:
            await ctx.send_me(f'Bot JÁ ESTÁ no canal {ctx.author.name}')
        else:
            CHAN.append(f'#{AUTHOR}')
            update_channel(CHAN)
            file_check(AUTHOR)
            await bot.join_channels(CHAN)
            await ctx.send_me(f'Bot ENTROU no canal {ctx.author.name}')


@bot.command(name='sair')
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHAN:
            CHAN.remove(f'#{AUTHOR}')
            update_channel(CHAN)
            await bot.part_channels([AUTHOR])
            await ctx.send_me(F'Bot SAIU do canal {ctx.author.name}')
        else:
            await ctx.send_me(F'Bot NÃO ESTÁ no canal {ctx.author.name}')


@bot.command(name='elos')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    elo = get_elo('', CHANNEL)
    div = get_div('', CHANNEL)
    conta = get_conta('', CHANNEL)
    elo1 = get_elo('1', CHANNEL)
    div1 = get_div('1', CHANNEL)
    conta1 = get_conta('1', CHANNEL)
    await ctx.send_me(f'{conta}: {elo} {div} | {conta1}: {elo1} {div1}')


@bot.command(name='conta')
async def command_conta(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!conta', '').strip()
            conta = 'Conta'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('conta', conta, CHANNEL)
            await ctx.send_me(f'Nome da conta atualizado para: {conta}')


@bot.command(name='elo')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!elo', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo', elo, CHANNEL)
            conta = get_conta('', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('', CHANNEL)
        div = get_div('', CHANNEL)
        pdl = get_pdl('', CHANNEL)
        drt = get_drt('', CHANNEL)
        conta = get_conta('', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='div')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!div', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            await ctx.send_me('Valor inválido')
            return
        update_value('div', div, CHANNEL)
        conta = get_conta('', CHANNEL)
        await ctx.send_me(f'Divisão da {conta} atualizada para {div}')


@bot.command(name='pdl')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!pdl', '').strip()
        try:
            pdl = get_pdl('', CHANNEL)
        except KeyError:
            pdl = 0
        if command_string.startswith('+'):
            val = command_string.replace('+', '').strip()
            try:
                pdl += int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl', pdl, CHANNEL)
            elo = get_elo('', CHANNEL)
            div = get_div('', CHANNEL)
            drt = get_drt('', CHANNEL)
            conta = get_conta('', CHANNEL)
        elif command_string.startswith('-'):
            val = command_string.replace('-', '').strip()
            try:
                pdl -= int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl', pdl, CHANNEL)
            elo = get_elo('', CHANNEL)
            div = get_div('', CHANNEL)
            drt = get_drt('', CHANNEL)
            conta = get_conta('', CHANNEL)
        else:
            try:
                pdl = int(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl', pdl, CHANNEL)
            elo = get_elo('', CHANNEL)
            div = get_div('', CHANNEL)
            drt = get_drt('', CHANNEL)
            conta = get_conta('', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='conta1')
async def command_conta(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!conta1', '').strip()
            conta = 'Conta1'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('conta1', conta, CHANNEL)
            await ctx.send_me(f'Nome da conta1 atualizado para: {conta}')


@bot.command(name='elo1')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!elo1', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo1', elo, CHANNEL)
            conta = get_conta('1', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('1', CHANNEL)
        div = get_div('1', CHANNEL)
        pdl = get_pdl('1', CHANNEL)
        drt = get_drt('1', CHANNEL)
        conta = get_conta('1', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='smurf')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!smurf', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo1', elo, CHANNEL)
            conta = get_conta('1', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('1', CHANNEL)
        div = get_div('1', CHANNEL)
        pdl = get_pdl('1', CHANNEL)
        drt = get_drt('1', CHANNEL)
        conta = get_conta('1', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='elosmurf')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!elosmurf', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo1', elo, CHANNEL)
            conta = get_conta('1', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('1', CHANNEL)
        div = get_div('1', CHANNEL)
        pdl = get_pdl('1', CHANNEL)
        drt = get_drt('1', CHANNEL)
        conta = get_conta('1', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='div1')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!div1', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            await ctx.send_me('Valor inválido')
            return
        update_value('div1', div, CHANNEL)
        conta = get_conta('1', CHANNEL)
        await ctx.send_me(f'Divisão da {conta} atualizada para {div}')


@bot.command(name='pdl1')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!pdl1', '').strip()
        try:
            pdl = get_pdl('1', CHANNEL)
        except KeyError:
            pdl = 0
        if command_string.startswith('+'):
            val = command_string.replace('+', '').strip()
            try:
                pdl += int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl1', pdl, CHANNEL)
            elo = get_elo('1', CHANNEL)
            div = get_div('1', CHANNEL)
            drt = get_drt('1', CHANNEL)
            conta = get_conta('1', CHANNEL)
        elif command_string.startswith('-'):
            val = command_string.replace('-', '').strip()
            try:
                pdl -= int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl1', pdl, CHANNEL)
            elo = get_elo('1', CHANNEL)
            div = get_div('1', CHANNEL)
            drt = get_drt('1', CHANNEL)
            conta = get_conta('1', CHANNEL)
        else:
            try:
                pdl = int(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl1', pdl, CHANNEL)
            elo = get_elo('1', CHANNEL)
            div = get_div('1', CHANNEL)
            drt = get_drt('1', CHANNEL)
            conta = get_conta('1', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')

@bot.command(name='conta2')
async def command_conta(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!conta2', '').strip()
            conta = 'Conta2'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('conta2', conta, CHANNEL)
            await ctx.send_me(f'Nome da conta2 atualizado para: {conta}')

@bot.command(name='elo2')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!elo2', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo2', elo, CHANNEL)
            conta = get_conta('2', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('2', CHANNEL)
        div = get_div('2', CHANNEL)
        pdl = get_pdl('2', CHANNEL)
        drt = get_drt('2', CHANNEL)
        conta = get_conta('2', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='div2')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!div2', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            await ctx.send_me('Valor inválido')
            return
        update_value('div2', div, CHANNEL)
        conta = get_conta('2', CHANNEL)
        await ctx.send_me(f'Divisão da {conta} atualizada para {div}')


@bot.command(name='pdl2')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!pdl2', '').strip()
        try:
            pdl = get_pdl('2', CHANNEL)
        except KeyError:
            pdl = 0
        if command_string.startswith('+'):
            val = command_string.replace('+', '').strip()
            try:
                pdl += int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl2', pdl, CHANNEL)
            elo = get_elo('2', CHANNEL)
            div = get_div('2', CHANNEL)
            drt = get_drt('2', CHANNEL)
            conta = get_conta('2', CHANNEL)
        elif command_string.startswith('-'):
            val = command_string.replace('-', '').strip()
            try:
                pdl -= int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl2', pdl, CHANNEL)
            elo = get_elo('2', CHANNEL)
            div = get_div('2', CHANNEL)
            drt = get_drt('2', CHANNEL)
            conta = get_conta('2', CHANNEL)
        else:
            try:
                pdl = int(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl2', pdl, CHANNEL)
            elo = get_elo('2', CHANNEL)
            div = get_div('2', CHANNEL)
            drt = get_drt('2', CHANNEL)
            conta = get_conta('2', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='conta3')
async def command_conta(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!conta3', '').strip()
            conta = 'Conta3'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('conta3', conta, CHANNEL)
            await ctx.send_me(f'Nome da conta3 atualizado para: {conta}')


@bot.command(name='elo3')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.content
            command_string = command_string.replace('!elo3', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('elo3', elo, CHANNEL)
            conta = get_conta('3', CHANNEL)
            await ctx.send_me(f'Elo da {conta} atualizado para {elo}')

    else:
        elo = get_elo('3', CHANNEL)
        div = get_div('3', CHANNEL)
        pdl = get_pdl('3', CHANNEL)
        drt = get_drt('3', CHANNEL)
        conta = get_conta('3', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


@bot.command(name='div3')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!div3', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            await ctx.send_me('Valor inválido')
            return
        update_value('div3', div, CHANNEL)
        conta = get_conta('3', CHANNEL)
        await ctx.send_me(f'Divisão da {conta} atualizada para {div}')


@bot.command(name='pdl3')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
        command_string = ctx.content
        command_string = command_string.replace('!pdl3', '').strip()
        try:
            pdl = get_pdl('3', CHANNEL)
        except KeyError:
            pdl = 0
        if command_string.startswith('+'):
            val = command_string.replace('+', '').strip()
            try:
                pdl += int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl3', pdl, CHANNEL)
            elo = get_elo('3', CHANNEL)
            div = get_div('3', CHANNEL)
            drt = get_drt('3', CHANNEL)
            conta = get_conta('3', CHANNEL)
        elif command_string.startswith('-'):
            val = command_string.replace('-', '').strip()
            try:
                pdl -= int(val)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl3', pdl, CHANNEL)
            elo = get_elo('3', CHANNEL)
            div = get_div('3', CHANNEL)
            drt = get_drt('3', CHANNEL)
            conta = get_conta('3', CHANNEL)
        else:
            try:
                pdl = int(command_string)
            except ValueError:
                await ctx.send_me('Valor inválido')
                return
            update_value('pdl3', pdl, CHANNEL)
            elo = get_elo('3', CHANNEL)
            div = get_div('3', CHANNEL)
            drt = get_drt('3', CHANNEL)
            conta = get_conta('3', CHANNEL)
        await ctx.send_me(f'{conta}: {elo} {div} ({pdl} {drt})')


def get_drt(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        cmd = data[f'elo{ac}'].lower()
        if cmd == 'ferro' or cmd == 'iron' or cmd == 'prata' or cmd == 'silver' or cmd == 'ouro' or cmd == 'gold' or cmd == 'plat' or cmd == 'platina' or cmd == 'platinum' or cmd == 'esmeralda' or cmd == 'emerald':
            drt = 'DoritosChip '
        else:
            drt = 'PdL'
        return drt


def get_elo(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'elo{ac}']


def get_conta(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'conta{ac}']


def get_div(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'div{ac}']


def get_pdl(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'pdl{ac}']


def update_value(key, value, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data[key] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def file_check(channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    if os.path.isfile(JSON_FILE) and os.access(JSON_FILE, os.R_OK):
        return True
    else:
        with io.open(os.path.join(JSON_FILE), 'w') as json_file:
            json_file.write(json.dumps({}))


if __name__ == "__main__":
    bot.run()
