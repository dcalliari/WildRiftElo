import os
import time
import threading
import static.python.db as db

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
CHANNELS = db.get_channel()
BOT_NICK = os.environ.get('BOT_NICK')

client = Client(
    token=TOKEN,
    heartbeat=30.0
)


def cooldown(function, duration=int(5)):
    function.on_cooldown = False

    def sleeper():
        function.on_cooldown = True
        time.sleep(duration)
        function.on_cooldown = False

    async def wrapper(*args, **kwargs):
        if function.on_cooldown:
            print(f"Function {function.__name__} on cooldown")
        else:
            timer = threading.Thread(target=sleeper)
            await function(*args, **kwargs)
            timer.start()
    return wrapper


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            prefix=PREFIX,
            token=TOKEN,
            initial_channels=CHANNELS,
            heartbeat=30.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')

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
    @cooldown
    async def command_elos(self, ctx: commands.Context):
        canal = ctx.channel.name
        try:
            elo = db.get(0, canal, 'elo')
            div = db.get(0, canal, 'div')
            conta = db.get(0, canal, 'conta')
            elo1 = db.get(1, canal, 'elo')
            div1 = db.get(1, canal, 'div')
            conta1 = db.get(1, canal, 'conta')
            elo2 = db.get(2, canal, 'elo')
            div2 = db.get(2, canal, 'div')
            conta2 = db.get(2, canal, 'conta')
            elo3 = db.get(3, canal, 'elo')
            div3 = db.get(3, canal, 'div')
            conta3 = db.get(3, canal, 'conta')
            await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
        except KeyError:
            try:
                elo = db.get(0, canal, 'elo')
                div = db.get(0, canal, 'div')
                conta = db.get(0, canal, 'conta')
                elo1 = db.get(1, canal, 'elo')
                div1 = db.get(1, canal, 'div')
                conta1 = db.get(1, canal, 'conta')
                elo2 = db.get(2, canal, 'elo')
                div2 = db.get(2, canal, 'div')
                conta2 = db.get(2, canal, 'conta')
                await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
            except KeyError:
                try:
                    elo = db.get(0, canal, 'elo')
                    div = db.get(0, canal, 'div')
                    conta = db.get(0, canal, 'conta')
                    elo1 = db.get(1, canal, 'elo')
                    div1 = db.get(1, canal, 'div')
                    conta1 = db.get(1, canal, 'conta')
                    await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1}')
                except KeyError:
                    try:
                        elo1 = db.get(1, canal, 'elo')
                        div1 = db.get(1, canal, 'div')
                        conta1 = db.get(1, canal, 'conta')
                        elo2 = db.get(2, canal, 'elo')
                        div2 = db.get(2, canal, 'div')
                        conta2 = db.get(2, canal, 'conta')
                        elo3 = db.get(3, canal, 'elo')
                        div3 = db.get(3, canal, 'div')
                        conta3 = db.get(3, canal, 'conta')
                        await ctx.reply(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
                    except KeyError:
                        try:
                            elo1 = db.get(1, canal, 'elo')
                            div1 = db.get(1, canal, 'div')
                            conta1 = db.get(1, canal, 'conta')
                            elo2 = db.get(2, canal, 'elo')
                            div2 = db.get(2, canal, 'div')
                            conta2 = db.get(2, canal, 'conta')
                            await ctx.reply(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
                        except KeyError:
                            await ctx.reply('/me Você precisa configurar pelo menos duas contas.')

    # Edita o nome das contas
    @commands.command(name='conta', aliases=['conta1', 'conta2', 'conta3', 'smurf', 'elosmurf'])
    @cooldown
    async def command_account(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'a' else ac
        ac = 1 if ac == 'f' else ac
        if ctx.message.content.split(' ')[1:] != [] and (ctx.author.is_mod or ctx.author.name == '1bode'):
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            conta = f'Conta{ac}'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.reply('/me Valor inválido')
                return
            db.update_riot_id(ac, conta, canal)
            ac = '' if ac == 0 else ac
            await ctx.reply(f'/me Nome da conta{ac} atualizado para: {conta}')

    # Edita o elo das contas ou responde com o elo
    @commands.command(name='elo', aliases=['elo1', 'elo2', 'elo3'])
    @cooldown
    async def command_elo(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'o' else ac
        if ctx.message.content.split(' ')[1:] != []:
            if ctx.author.is_mod or ctx.author.name == '1bode':
                command_string = ctx.message.content.split(' ', 1)[1:][0]
                elo = 'Ferro'
                try:
                    elo = str(command_string)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                db.update_elo(ac, elo, canal)
                conta = db.get(ac, canal, 'conta')
                await ctx.reply(f'/me Elo de "{conta}" atualizado para {elo}')

        else:
            elo = db.get(ac, canal, 'elo')
            div = db.get(ac, canal, 'div')
            pdl = db.get(ac, canal, 'pdl')
            drt = db.get(ac, canal, 'drt')
            conta = db.get(ac, canal, 'conta')
            await ctx.reply(f'/me {conta}: {elo} {div} ({pdl} {drt})')

    # Edita a divisão das contas
    @commands.command(name='div', aliases=['div1', 'div2', 'div3'])
    @cooldown
    async def command_div(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'v' else ac
        if ctx.author.is_mod or ctx.author.name == '1bode':
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            div = 0
            try:
                div = int(command_string)
            except ValueError:
                await ctx.reply('/me Valor inválido')
                return
            db.update_div(ac, div, canal)
            conta = db.get(ac, canal, 'conta')
            await ctx.reply(f'/me Divisão de "{conta}" atualizada para {div}')

    # Edita os pontos/doritos das contas
    @commands.command(name='pdl', aliases=['pdl1', 'pdl2', 'pdl3'])
    @cooldown
    async def command_pdl(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'l' else ac
        if ctx.author.is_mod or ctx.author.name == '1bode':
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            try:
                pdl = db.get(ac, canal, 'pdl')
            except KeyError:
                pdl = 0
            if command_string.startswith('+'):
                val = command_string.replace('+', '').strip()
                try:
                    pdl += int(val)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                db.update_pdl(ac, pdl, canal)
                elo = db.get(ac, canal, 'elo')
                div = db.get(ac, canal, 'div')
                drt = db.get(ac, canal, 'drt')
                conta = db.get(ac, canal, 'conta')
            elif command_string.startswith('-'):
                val = command_string.replace('-', '').strip()
                try:
                    pdl -= int(val)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                db.update_pdl(ac, pdl, canal)
                elo = db.get(ac, canal, 'elo')
                div = db.get(ac, canal, 'div')
                drt = db.get(ac, canal, 'drt')
                conta = db.get(ac, canal, 'conta')
            else:
                try:
                    pdl = int(command_string)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                db.update_pdl(ac, pdl, canal)
                elo = db.get(ac, canal, 'elo')
                div = db.get(ac, canal, 'div')
                drt = db.get(ac, canal, 'drt')
                conta = db.get(ac, canal, 'conta')
            await ctx.reply(f'/me {conta}: {elo} {div} ({pdl} {drt})')

    # Envia o link do tutorial caso esteja no canal do bot, caso contrário, envia instruções
    @commands.command(name='tutorial', aliases=['tuto'])
    @cooldown
    async def command_tutorial(self, ctx: commands.Context):
        if ctx.channel.name == BOT_NICK:
            await ctx.reply('/me Como adicionar o bot e configurar em seu canal: https://imgur.com/a/zl1T2CY')
        else:
            await ctx.reply(f'/me Envie !tutorial no chat do {BOT_NICK}')

    # Entra no canal que enviou a mensagem
    @commands.command(name='join', aliases=['entrar'])
    async def command_join(self, ctx: commands.Context):
        autor = ctx.author.name
        print(autor)
        if autor == '1bode':
            try:
                autor = ctx.message.content.split()[1]
                print(autor)
            except IndexError:
                pass
        elif ctx.channel.name == BOT_NICK:
            print(autor)
            if db.add_channel(autor) == -1:
                await ctx.reply(f'/me Bot JÁ ESTÁ no canal {autor}')
            else:
                await ctx.reply(f'/me Bot ENTROU no canal {autor}')

    # Sai do canal que enviou a mensagem
    @commands.command(name='leave', aliases=['sair'])
    async def command_leave(self, ctx: commands.Context):
        autor = ctx.author.name
        if autor == '1bode':
            try:
                autor = ctx.message.content.split()[1]
            except IndexError:
                pass
        elif ctx.channel.name == BOT_NICK:
            if db.del_channel(autor) == -1:
                await ctx.reply(F'/me Bot NÃO ESTÁ no canal {autor}')
            else:
                await ctx.reply(F'/me Bot SAIU do canal {autor}')


bot = Bot()

# # comando para git pull pelo chat
# @commands.command(name="update")
# async def update(ctx):
#     if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
#         os.system("git pull")
#         print("Atualizando e reiniciando...")
#         os.system("python3 bot.py")
#         exit()
