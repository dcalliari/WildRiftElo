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
CHANNEL = json.loads(os.environ['CHANNEL'])
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNEL
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


@bot.command(name='elo')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL):
            command_string = ctx.content
            command_string = command_string.replace('!elo', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                elo = 'Ferro'
            update_value('elo', elo, CHANNEL)
            await ctx.send_me(f'Elo mudou pra {elo}')

    else:
        elo = get_elo('', CHANNEL)
        div = get_div('', CHANNEL)
        pdl = get_pdl('', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='div')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!div', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            div = 0
        update_value('div', div, CHANNEL)
        await ctx.send_me(f'Divisão mudou pra {div}')


@bot.command(name='pdl')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!pdl', '').strip()
        pdl = 0
        try:
            pdl = int(command_string)
        except ValueError:
            pdl = 0
        update_value('pdl', pdl, CHANNEL)
        elo = get_elo('', CHANNEL)
        div = get_div('', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='elo1')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL):
            command_string = ctx.content
            command_string = command_string.replace('!elo1', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                elo = 'Ferro'
            update_value('elo1', elo, CHANNEL)
            await ctx.send_me(f'Elo mudou pra {elo}')

    else:
        elo = get_elo('1', CHANNEL)
        div = get_div('1', CHANNEL)
        pdl = get_pdl('1', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='div1')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!div1', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            div = 0
        update_value('div1', div, CHANNEL)
        await ctx.send_me(f'Divisão mudou pra {div}')


@bot.command(name='pdl1')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!pdl1', '').strip()
        pdl = 0
        try:
            pdl = int(command_string)
        except ValueError:
            pdl = 0
        update_value('pdl1', pdl, CHANNEL)
        elo = get_elo('1', CHANNEL)
        div = get_div('1', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='elo2')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL):
            command_string = ctx.content
            command_string = command_string.replace('!elo2', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                elo = 'Ferro'
            update_value('elo2', elo, CHANNEL)
            await ctx.send_me(f'Elo mudou pra {elo}')

    else:
        elo = get_elo('2', CHANNEL)
        div = get_div('2', CHANNEL)
        pdl = get_pdl('2', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='div2')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!div2', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            div = 0
        update_value('div2', div, CHANNEL)
        await ctx.send_me(f'Divisão mudou pra {div}')


@bot.command(name='pdl2')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!pdl2', '').strip()
        pdl = 0
        try:
            pdl = int(command_string)
        except ValueError:
            pdl = 0
        update_value('pdl2', pdl, CHANNEL)
        elo = get_elo('2', CHANNEL)
        div = get_div('2', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')

@bot.command(name='elo3')
async def command_elo(ctx):
    CHANNEL = ctx.channel.name.lower()
    if ctx.content.split(' ')[1:] != []:
        if(ctx.author.is_mod) or (ctx.author == CHANNEL):
            command_string = ctx.content
            command_string = command_string.replace('!elo3', '').strip()
            elo = 'Ferro'
            try:
                elo = str(command_string)
            except ValueError:
                elo = 'Ferro'
            update_value('elo3', elo, CHANNEL)
            await ctx.send_me(f'Elo mudou pra {elo}')

    else:
        elo = get_elo('3', CHANNEL)
        div = get_div('3', CHANNEL)
        pdl = get_pdl('3', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


@bot.command(name='div3')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!div3', '').strip()
        div = 0
        try:
            div = int(command_string)
        except ValueError:
            div = 0
        update_value('div3', div, CHANNEL)
        await ctx.send_me(f'Divisão mudou pra {div}')


@bot.command(name='pdl3')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!pdl3', '').strip()
        pdl = 0
        try:
            pdl = int(command_string)
        except ValueError:
            pdl = 0
        update_value('pdl3', pdl, CHANNEL)
        elo = get_elo('3', CHANNEL)
        div = get_div('3', CHANNEL)
        await ctx.send_me(f'{elo} {div} ({pdl} PdL)')


def get_elo(ac, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data[f'elo{ac}']


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


if __name__ == "__main__":
    bot.run()
