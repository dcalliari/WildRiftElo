import os
import asyncio
import static.python.db_modules as mod

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
BOT_NICK = os.environ.get('BOT_NICK')

client = Client(
    token=TOKEN,
    heartbeat=20.0
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            prefix=PREFIX,
            token=TOKEN,
            initial_channels=[BOT_NICK],
            heartbeat=20.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')
        conn = []
        j = 0
        channels = await mod.get_channels()
        len_channels = len(channels)
        for i in range(int(len_channels/20)+1):
            if i < int(len(channels)/20):
                while len(conn) < 20:
                    conn.append(channels[j])
                    j += 1
                await bot.join_channels(conn)
                await asyncio.sleep(30)
            else:
                while len(conn) < len_channels % 20:
                    conn.append(channels[j])
                    j += 1
                await bot.join_channels(conn)
            conn = []

    async def event_message(self, message):

        if message.echo:
            return

        autor = message.author.name
        canal = message.channel.name
        content = message.content
        hora = message.timestamp.strftime('%H:%M:%S')
        print(f'#{canal} {hora} {autor}: {content}')

        await self.handle_commands(message)

    # Add or edit account
    @commands.command(name='account', aliases=mod.lang()['global']['account']['aliases'])
    # @commands.cooldown(1, 1)
    async def command_account(self, ctx: commands.Context):
        if ctx.message.content.split(' ')[1:] != [] and (ctx.author.is_mod or ctx.author.name in mod.lang()['global']['admin']):
            canal = ctx.channel.name
            lang = mod.lang()[await mod.get_lang(canal)]['account']
            id = ctx.message.content.split(' ', 1)[0][-1]
            try:
                id = int(id)
            except:
                id = 0
            riotId = ctx.message.content.split(' ', 1)[1:][0]
            if await mod.idCheck(riotId):
                await ctx.reply(lang['delay'])
                accId = await mod.createHash(riotId)
                if accId != 'gameid':
                    await mod.update_riot_id(id, accId, canal)
                    id = '' if id == 0 else id
                    await ctx.reply(lang['updated'] % (id, riotId))
                else:
                    await ctx.reply(lang['error'])
            else:
                await ctx.reply(lang['invalid'])

    @commands.command(name='delaccount', aliases=mod.lang()['global']['delaccount']['aliases'])
    async def command_delete(self, ctx: commands.Context):
        canal = ctx.channel.name
        lang = mod.lang()[await mod.get_lang(canal)]['delaccount']
        id = ctx.message.content.split(' ', 1)[0][-1]
        try:
            id = int(id)
        except:
            id = 0
        if await mod.del_account(id, canal):
            id = '' if id == 0 else id
            await ctx.reply(lang['deleted'] % id)
        else:
            id = '' if id == 0 else id
            await ctx.reply(lang['not_found'] % id)

    # Sends elo in chat
    @commands.command(name='elo', aliases=mod.lang()['global']['elo']['aliases'])
    @commands.cooldown(1, 5)
    async def command_elo(self, ctx: commands.Context):
        canal = ctx.channel.name
        if canal != 'loraakl':
            lang = mod.lang()[await mod.get_lang(canal)]['elo']
            id = ctx.message.content.split(' ', 1)[0][-1]
            id = 1 if id == 'f' else id
            try:
                id = int(id)
            except:
                id = 0
            try:
                response = await mod.get_elo(id, canal)
                await ctx.send(f'/me {response}')
            except AttributeError:
                contas = await mod.get_accounts(canal, 'elo')
                id = await mod.get_accounts(canal, 'id')
                if len(contas) == 0:
                    await ctx.reply(lang['no_accounts'])
                else:
                    response1 = ' | '.join(contas)
                    response2 = ' !elo'.join(
                        '' if x == 0 else str(x) for x in id)
                    await ctx.send(f'/me {response1}')
                    await ctx.reply(lang['available_accounts'] % response2)

    # For streamers who opt for elowr
    @commands.command(name='elowr', aliases=["elowr1", "elowr2", "elowr3"])
    # @commands.cooldown(1, 5)
    async def command_elowr(self, ctx: commands.Context):
        canal = ctx.channel.name
        if canal == 'loraakl':
            lang = mod.lang()[await mod.get_lang(canal)]['elo']
            id = ctx.message.content.split(' ', 1)[0][-1]
            id = 0 if id == 'r' else id
            try:
                response = await mod.get_elo(id, canal)
                await ctx.send(f'/me {response}')
            except AttributeError:
                contas = await mod.get_accounts(canal, 'elo')
                id = await mod.get_accounts(canal, 'id')
                if len(contas) == 0:
                    await ctx.reply(lang['no_accounts'])
                else:
                    response1 = ' | '.join(contas)
                    response2 = ' !elo'.join(
                        '' if x == 0 else str(x) for x in id)
                    await ctx.send(f'/me {response1}')
                    await ctx.reply(lang['available_accounts'] % response2)

    # Show elos from all accounts
    @commands.command(name='elos', aliases=mod.lang()['global']['elos']['aliases'])
    # @commands.cooldown(1, 5)
    async def command_elos(self, ctx: commands.Context):
        canal = ctx.channel.name
        lang = mod.lang()[await mod.get_lang(canal)]['elos']
        try:
            contas = await mod.get_accounts(canal, 'elo')
            if len(contas) > 1:
                response = ' | '.join(contas)
                await ctx.send(f'/me {response}')
            else:
                await ctx.reply(lang['no_accounts'])
        except:
            await ctx.reply(lang['no_accounts'])

    # Send instructions
    @commands.command(name='elohelp', aliases=mod.lang()['global']['elohelp']['aliases'])
    # @commands.cooldown(1, 3)
    async def command_help(self, ctx: commands.Context):
        lang = mod.lang()[await mod.get_lang(ctx.channel.name)]['elohelp']
        if ctx.channel.name == BOT_NICK:
            await ctx.reply(lang['bot_channel'])
        else:
            await ctx.reply(lang['user_channel'])

    # Change bot language
    @commands.command(name='lang')
    # @commands.cooldown(1, 3)
    async def command_language(self, ctx: commands.Context):
        if ctx.author.is_mod or ctx.author.name in mod.lang()['global']['admin']:
            canal = ctx.channel.name
            lang = mod.lang()[await mod.get_lang(canal)]['lang']
            lang_keys = list(mod.lang().keys())[1:]
            key_string = ', '.join(lang_keys)
            try:
                l = ctx.message.content.split(' ')[1]
            except IndexError:
                await ctx.reply(lang['instructions'] % key_string)
                return
            if l in lang_keys and l != 'global':
                await mod.change_lang(l, canal)
                await ctx.reply(lang['updated'] % l)
            else:
                await ctx.reply(lang['wrong_lang'] % key_string)
                return

    # Enters the channel which sent the message
    @commands.command(name='join', aliases=mod.lang()['global']['join']['aliases'])
    @commands.cooldown(1, 5)
    async def command_join(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor in mod.lang()['global']['admin']:
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor in await mod.get_channels():
                await ctx.send(f'/me Bot is already in the channel: {autor}. Send /vip WildRiftElo in your chat then !elohelp')
            else:
                await mod.add_channel(autor)
                await bot.join_channels([autor])
                await ctx.send(f'/me Bot joined the channel: {autor}. Send /vip WildRiftElo in your chat then !elohelp')

    # Leaves the channel which sent the message
    @commands.command(name='leave', aliases=mod.lang()['global']['leave']['aliases'])
    @commands.cooldown(1, 5)
    async def command_leave(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor in mod.lang()['global']['admin']:
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor not in await mod.get_channels():
                await ctx.send(f'/me Bot is not in the channel: {autor}')
            else:
                await mod.del_channel(autor)
                await ctx.send(f'/me Bot left the channel: {autor}')

    # Git Pull and reboot via chat
    @commands.command(name="update")
    async def command_update(self, ctx: commands.Context):
        if ctx.author.name in mod.lang()['global']['admin']:
            await ctx.send('/me Updating!')
            os.system("git pull")
            print("Updating and rebooting...")
            os.system("python3 main.py")
            exit()


bot = Bot()
