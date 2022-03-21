import os
import static.python.mod as mod

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.client import Client

load_dotenv(os.path.abspath('.env'))

PREFIX = os.environ.get('BOT_PREFIX')
TOKEN = os.environ.get('TOKEN')
CHANNELS = mod.get_channel()
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
    @mod.cooldown
    async def command_elo(self, ctx: commands.Context):
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
            await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
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
                await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
            except KeyError:
                try:
                    elo = mod.get_elo('', CHANNEL)
                    div = mod.get_div('', CHANNEL)
                    conta = mod.get_conta('', CHANNEL)
                    elo1 = mod.get_elo('1', CHANNEL)
                    div1 = mod.get_div('1', CHANNEL)
                    conta1 = mod.get_conta('1', CHANNEL)
                    await ctx.reply(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1}')
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
                        await ctx.reply(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
                    except KeyError:
                        try:
                            elo1 = mod.get_elo('1', CHANNEL)
                            div1 = mod.get_div('1', CHANNEL)
                            conta1 = mod.get_conta('1', CHANNEL)
                            elo2 = mod.get_elo('2', CHANNEL)
                            div2 = mod.get_div('2', CHANNEL)
                            conta2 = mod.get_conta('2', CHANNEL)
                            await ctx.reply(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
                        except KeyError:
                            await ctx.reply('/me Você precisa configurar pelo menos duas contas.')

    # Edita o nome das contas
    @commands.command(name='conta', aliases=['conta1', 'conta2', 'conta3', 'smurf', 'elosmurf'])
    @mod.cooldown
    async def command_conta(self, ctx: commands.Context):
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
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_value(f'conta{ac}', conta, CHANNEL)
                await ctx.reply(f'/me Nome da conta{ac} atualizado para: {conta}')

    # Edita o elo das contas ou responde com o elo
    @commands.command(name='elo', aliases=['elo1', 'elo2', 'elo3'])
    @mod.cooldown
    async def command_elo(self, ctx: commands.Context):
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
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_value(f'elo{ac}', elo, CHANNEL)
                conta = mod.get_conta(ac, CHANNEL)
                await ctx.reply(f'/me Elo de "{conta}" atualizado para {elo}')

        else:
            elo = mod.get_elo(ac, CHANNEL)
            div = mod.get_div(ac, CHANNEL)
            pdl = mod.get_pdl(ac, CHANNEL)
            drt = mod.get_drt(ac, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
            await ctx.reply(f'/me {conta}: {elo} {div} ({pdl} {drt})')

    # Edita a divisão das contas
    @commands.command(name='div', aliases=['div1', 'div2', 'div3'])
    @mod.cooldown
    async def command_add(self, ctx: commands.Context):
        CHANNEL = ctx.channel.name.lower()
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = '' if ac == 'v' else ac
        if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            div = 0
            try:
                div = int(command_string)
            except ValueError:
                await ctx.reply('/me Valor inválido')
                return
            mod.update_value(f'div{ac}', div, CHANNEL)
            conta = mod.get_conta(ac, CHANNEL)
            await ctx.reply(f'/me Divisão de "{conta}" atualizada para {div}')

    # Edita os pontos/doritos das contas
    @commands.command(name='pdl', aliases=['pdl1', 'pdl2', 'pdl3'])
    @mod.cooldown
    async def command_add(self, ctx: commands.Context):
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
                    await ctx.reply('/me Valor inválido')
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
                    await ctx.reply('/me Valor inválido')
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
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_value(f'pdl{ac}', pdl, CHANNEL)
                elo = mod.get_elo(ac, CHANNEL)
                div = mod.get_div(ac, CHANNEL)
                drt = mod.get_drt(ac, CHANNEL)
                conta = mod.get_conta(ac, CHANNEL)
            await ctx.reply(f'/me {conta}: {elo} {div} ({pdl} {drt})')

    # Envia o link do tutorial caso esteja no canal do bot, caso contrário, envia instruções
    @commands.command(name='tutorial', aliases=['tuto'])
    @mod.cooldown
    async def command_tutorial(self, ctx: commands.Context):
        if ctx.channel.name.lower() == BOT_NICK.lower():
            await ctx.reply('/me Como adicionar o bot e configurar em seu canal: https://imgur.com/a/zl1T2CY')
        else:
            await ctx.reply(f'/me Envie !tutorial no chat do {BOT_NICK}')

    # Entra no canal que enviou a mensagem
    @commands.command(name='join', aliases=['entrar'])
    async def command_join(self, ctx: commands.Context):
        AUTHOR = ctx.author.name.lower()
        if AUTHOR == '1bode':
            try:
                AUTHOR = ctx.message.content.split()[1]
            except IndexError:
                pass
        elif ctx.channel.name.lower() == BOT_NICK.lower():
            if mod.add_channel(AUTHOR) == -1:
                await ctx.reply(f'/me Bot JÁ ESTÁ no canal {AUTHOR}')
            else:
                await ctx.reply(f'/me Bot ENTROU no canal {AUTHOR}')

    # Sai do canal que enviou a mensagem
    @commands.command(name='leave', aliases=['sair'])
    async def command_leave(self, ctx: commands.Context):
        AUTHOR = ctx.author.name.lower()
        if AUTHOR == '1bode':
            try:
                AUTHOR = ctx.message.content.split()[1]
            except IndexError:
                pass
        elif ctx.channel.name.lower() == BOT_NICK.lower():
            if mod.del_channel(AUTHOR) == -1:
                await ctx.reply(F'/me Bot NÃO ESTÁ no canal {AUTHOR}')
            else:
                await ctx.reply(F'/me Bot SAIU do canal {AUTHOR}')


bot = Bot()

# # comando para git pull pelo chat
# @commands.command(name="update")
# async def update(ctx):
#     if ctx.author.name == 'bodedotexe' or ctx.author.name == '1bode':
#         os.system("git pull")
#         print("Atualizando e reiniciando...")
#         os.system("python3 bot.py")
#         exit()
