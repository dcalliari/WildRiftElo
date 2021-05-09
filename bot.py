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
CHANNEL = ['1bode','wildriftelo', 'bodedotexe']
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
        elo = get_elo(CHANNEL)
        div = get_div(CHANNEL)
        lp = get_lp(CHANNEL)
        await ctx.send_me(f'{elo} {div} ({lp} PdL)')


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
        await ctx.send(f'Divisão mudou pra {div}')

@bot.command(name='pdl')
async def command_add(ctx):
    CHANNEL = ctx.channel.name.lower()
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!pdl', '').strip()
        lp = 0
        try:
            lp = int(command_string)
        except ValueError:
            lp = 0
        update_value('lp', lp, CHANNEL)
        elo = get_elo(CHANNEL)
        div = get_div(CHANNEL)
        await ctx.send_me(f'{elo} {div} ({lp} PdL)')


def get_elo(channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['elo']


def get_div(channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['div']


def get_lp(channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + f'/channeldata/{channel}.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['lp']


def update_value(key, value, channel):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + f'/channeldata/{channel}.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data[key] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


if __name__ == "__main__":
    bot.run()
