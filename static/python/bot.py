import os
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
            initial_channels=mod.get_channel(),
            heartbeat=30.0
        )

    async def event_ready(self):
        print(f'Iniciando como | {self.nick}')
        print(f'Id de usuário é | {self.user_id}')
        # k = 0
        # j = 0
        # conn = []
        # channels = mod.get_channel()
        # if len(channels) > 20:
        #     for i in range(int(len(channels)/20)):
        #         while j < 20+k:
        #             conn.append(channels[j])
        #             j += 1
        #         await bot.join_channels(conn)
        #         time.sleep(20)
        #         k += 20
        # else:
        #     await bot.join_channels(channels)

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
    @commands.cooldown(1, 1)
    async def command_elos(self, ctx: commands.Context):
        canal = ctx.channel.name
        try:
            elo = mod.get(0, canal, 'elo')
            div = mod.get(0, canal, 'div')
            conta = mod.get(0, canal, 'conta')
            elo1 = mod.get(1, canal, 'elo')
            div1 = mod.get(1, canal, 'div')
            conta1 = mod.get(1, canal, 'conta')
            elo2 = mod.get(2, canal, 'elo')
            div2 = mod.get(2, canal, 'div')
            conta2 = mod.get(2, canal, 'conta')
            elo3 = mod.get(3, canal, 'elo')
            div3 = mod.get(3, canal, 'div')
            conta3 = mod.get(3, canal, 'conta')
            await ctx.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
        except AttributeError:
            try:
                elo = mod.get(0, canal, 'elo')
                div = mod.get(0, canal, 'div')
                conta = mod.get(0, canal, 'conta')
                elo1 = mod.get(1, canal, 'elo')
                div1 = mod.get(1, canal, 'div')
                conta1 = mod.get(1, canal, 'conta')
                elo2 = mod.get(2, canal, 'elo')
                div2 = mod.get(2, canal, 'div')
                conta2 = mod.get(2, canal, 'conta')
                await ctx.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
            except AttributeError:
                try:
                    elo = mod.get(0, canal, 'elo')
                    div = mod.get(0, canal, 'div')
                    conta = mod.get(0, canal, 'conta')
                    elo1 = mod.get(1, canal, 'elo')
                    div1 = mod.get(1, canal, 'div')
                    conta1 = mod.get(1, canal, 'conta')
                    await ctx.send(f'/me {conta}: {elo} {div} | {conta1}: {elo1} {div1}')
                except AttributeError:
                    try:
                        elo1 = mod.get(1, canal, 'elo')
                        div1 = mod.get(1, canal, 'div')
                        conta1 = mod.get(1, canal, 'conta')
                        elo2 = mod.get(2, canal, 'elo')
                        div2 = mod.get(2, canal, 'div')
                        conta2 = mod.get(2, canal, 'conta')
                        elo3 = mod.get(3, canal, 'elo')
                        div3 = mod.get(3, canal, 'div')
                        conta3 = mod.get(3, canal, 'conta')
                        await ctx.send(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2} | {conta3}: {elo3} {div3}')
                    except AttributeError:
                        try:
                            elo1 = mod.get(1, canal, 'elo')
                            div1 = mod.get(1, canal, 'div')
                            conta1 = mod.get(1, canal, 'conta')
                            elo2 = mod.get(2, canal, 'elo')
                            div2 = mod.get(2, canal, 'div')
                            conta2 = mod.get(2, canal, 'conta')
                            await ctx.send(f'/me {conta1}: {elo1} {div1} | {conta2}: {elo2} {div2}')
                        except AttributeError:
                            await ctx.reply('/me Você precisa configurar pelo menos duas contas.')

    # Edita o nome das contas
    @commands.command(name='conta', aliases=['conta1', 'conta2', 'conta3'])
    @commands.cooldown(1, 1)
    async def command_account(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'a' else ac
        if ctx.message.content.split(' ')[1:] != [] and (ctx.author.is_mod or ctx.author.name == '1bode'):
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            conta = f'Conta{ac}'
            try:
                conta = str(command_string)
            except ValueError:
                await ctx.reply('/me Valor inválido')
                return
            mod.update_riot_id(ac, conta, canal)
            ac = '' if ac == 0 else ac
            await ctx.reply(f'/me Nome da conta{ac} atualizado para: {conta}')

    # Edita o elo das contas ou responde com o elo
    @commands.command(name='elo', aliases=['elo1', 'elo2', 'elo3', 'smurf', 'elosmurf'])
    @commands.cooldown(1, 1)
    async def command_elo(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'o' else ac
        ac = 1 if ac == 'f' else ac
        if ctx.message.content.split(' ')[1:] != []:
            if ctx.author.is_mod or ctx.author.name == '1bode':
                command_string = ctx.message.content.split(' ', 1)[1:][0]
                elo = 'Ferro'
                try:
                    elo = str(command_string)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_elo(ac, elo, canal)
                conta = mod.get(ac, canal, 'conta')
                await ctx.reply(f'/me Elo de "{conta}" atualizado para {elo}')

        else:
            try:
                elo = mod.get(ac, canal, 'elo')
                div = mod.get(ac, canal, 'div')
                pdl = mod.get(ac, canal, 'pdl')
                drt = mod.get(ac, canal, 'drt')
                conta = mod.get(ac, canal, 'conta')
                if canal == 'lufelixya':
                    await ctx.send(f'/me {conta}: {elo} {div} ({pdl} {drt}) lufeliCalva')
                else:
                    await ctx.send(f'/me {conta}: {elo} {div} ({pdl} {drt})')
            except AttributeError:
                await ctx.reply(f'/me Primeiro você deve adicionar uma conta. Para mais informações, envie !tutorial no chat do bot.')

    # Edita a divisão das contas
    @commands.command(name='div', aliases=['div1', 'div2', 'div3'])
    @commands.cooldown(1, 3)
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
            mod.update_div(ac, div, canal)
            conta = mod.get(ac, canal, 'conta')
            await ctx.reply(f'/me Divisão de "{conta}" atualizada para {div}')

    # Edita os pontos/doritos das contas
    @commands.command(name='pdl', aliases=['pdl1', 'pdl2', 'pdl3'])
    @commands.cooldown(1, 3)
    async def command_pdl(self, ctx: commands.Context):
        canal = ctx.channel.name
        ac = ctx.message.content.split(' ', 1)[0][-1]
        ac = 0 if ac == 'l' else ac
        if ctx.author.is_mod or ctx.author.name == '1bode':
            command_string = ctx.message.content.split(' ', 1)[1:][0]
            try:
                pdl = mod.get(ac, canal, 'pdl')
            except KeyError:
                pdl = 0
            if command_string.startswith('+'):
                val = command_string.replace('+', '').strip()
                try:
                    pdl += int(val)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_pdl(ac, pdl, canal)
                elo = mod.get(ac, canal, 'elo')
                div = mod.get(ac, canal, 'div')
                drt = mod.get(ac, canal, 'drt')
                conta = mod.get(ac, canal, 'conta')
            elif command_string.startswith('-'):
                val = command_string.replace('-', '').strip()
                try:
                    pdl -= int(val)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_pdl(ac, pdl, canal)
                elo = mod.get(ac, canal, 'elo')
                div = mod.get(ac, canal, 'div')
                drt = mod.get(ac, canal, 'drt')
                conta = mod.get(ac, canal, 'conta')
            else:
                try:
                    pdl = int(command_string)
                except ValueError:
                    await ctx.reply('/me Valor inválido')
                    return
                mod.update_pdl(ac, pdl, canal)
                elo = mod.get(ac, canal, 'elo')
                div = mod.get(ac, canal, 'div')
                drt = mod.get(ac, canal, 'drt')
                conta = mod.get(ac, canal, 'conta')
            await ctx.send(f'/me {conta}: {elo} {div} ({pdl} {drt})')

    # Envia o link do tutorial caso esteja no canal do bot, caso contrário, envia instruções
    @commands.command(name='tutorial', aliases=['tuto'])
    @commands.cooldown(1, 3)
    async def command_tutorial(self, ctx: commands.Context):
        if ctx.channel.name == BOT_NICK:
            await ctx.reply('/me Como adicionar o bot e configurar em seu canal: https://imgur.com/a/zl1T2CY')
        else:
            await ctx.reply(f'/me Envie !tutorial no chat do {BOT_NICK}')

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
            if autor in mod.get_channel():
                await ctx.send(f'/me Bot JÁ ESTÁ no canal {autor}')
            else:
                if len(mod.get_channel()) < 20:
                    mod.add_channel(autor)
                    await bot.join_channels([autor])
                    await ctx.send(f'/me Bot ENTROU no canal {autor}')
                else:
                    await ctx.send(f'/me No momento não temos vaga :( @1bode tá tentando resolver!')

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
            if autor not in mod.get_channel():
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
