import os
import time
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
    heartbeat=30.0
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            prefix=PREFIX,
            token=TOKEN,
            initial_channels=[BOT_NICK],
            heartbeat=30.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')
        conn = []
        j = 0
        channels = mod.get_channels()
        len_channels = len(channels)
        for i in range(int(len_channels/20)+1):
            if i < int(len(channels)/20):
                while len(conn) < 20:
                    conn.append(channels[j])
                    j += 1
                await bot.join_channels(conn)
                time.sleep(30)
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

    # Mostra os elos de todas as contas
    @commands.command(name='elos')
    @commands.cooldown(1, 5)
    async def command_elos(self, ctx: commands.Context):
        try:
            contas = mod.get_accounts(ctx.channel.name)
            if len(contas) > 1:
                response = ' | '.join(contas)
                await ctx.send(f'/me {response}')
            else:
                await ctx.reply('/me Você precisa configurar pelo menos duas contas.')
        except:
            await ctx.reply('/me Você precisa configurar pelo menos duas contas.')

    # Edita o nome das contas
    @commands.command(name='conta', aliases=['conta1', 'conta2', 'conta3', 'account', 'account1', 'account2', 'account3'])
    @commands.cooldown(1, 1)
    async def command_account(self, ctx: commands.Context):
        id = ctx.message.content.split(' ', 1)[0][-1]
        id = 0 if id == 'a' else id
        id = 0 if id == 't' else id
        if ctx.message.content.split(' ')[1:] != [] and (ctx.author.is_mod or ctx.author.name == '1bode'):
            riotId = ctx.message.content.split(' ', 1)[1:][0]
            if mod.idCheck(riotId):
                await ctx.reply(f'Aguarde alguns segundos...')
                accId = mod.createHash(riotId)
                if accId != 'gameid':
                    mod.update_riot_id(id, accId, ctx.channel.name)
                    id = '' if id == 0 else id
                    await ctx.reply(f'/me Conta{id} atualizada para: {riotId}')
                else:
                    await ctx.reply('Não foi possível adicionar esta conta. Entre em contato com @1bode.')
            else:
                await ctx.reply('/me Valor inválido. Ex: Emerok#BR1')

    # Responde com o elo
    @commands.command(name='elo', aliases=['elomain', 'elo1', 'elo2', 'elo3', 'smurf', 'elosmurf'])
    @commands.cooldown(1, 5)
    async def command_elo(self, ctx: commands.Context):
        id = ctx.message.content.split(' ', 1)[0][-1]
        id = 0 if id == 'o' else id
        id = 0 if id == 'n' else id
        id = 1 if id == 'f' else id
        try:
            response = mod.get_elo(id, ctx.channel.name)
            await ctx.send(f'/me {response}')
        except AttributeError:
            await ctx.reply(f'/me Primeiro você deve adicionar uma conta. Envie !eloajuda')

    # Envia o link do tutorial caso esteja no canal do bot, caso contrário, envia instruções
    @commands.command(name='elohelp', aliases=['wrhelp', 'eloajuda'])
    @commands.cooldown(1, 3)
    async def command_tutorial(self, ctx: commands.Context):
        await ctx.reply(f'/me Configure sua primeira conta enviando !conta Account#Tag. Ex: !conta Emerok#BR1')

    # Entra no canal que enviou a mensagem
    @commands.command(name='join', aliases=['entrar'])
    async def command_join(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor == '1bode':
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor in mod.get_channels():
                await ctx.send(f'/me Bot JÁ ESTÁ no canal {autor}')
            else:
                mod.add_channel(autor)
                await bot.join_channels([autor])
                await ctx.send(f'/me Bot ENTROU no canal {autor}')

    # Sai do canal que enviou a mensagem
    @commands.command(name='leave', aliases=['sair'])
    async def command_leave(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor == '1bode':
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        if ctx.channel.name == BOT_NICK:
            if autor not in mod.get_channels():
                await ctx.send(F'/me Bot NÃO ESTÁ no canal {autor}')
            else:
                mod.del_channel(autor)
                await ctx.send(F'/me Bot SAIU do canal {autor}')

    # Comando para git pull pelo chat
    @commands.command(name="update")
    async def update(self, ctx: commands.Context):
        if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
            await ctx.send('Atualizando.')
            os.system("git pull")
            print("Atualizando e reiniciando...")
            os.system("python3 main.py")
            exit()


bot = Bot()
