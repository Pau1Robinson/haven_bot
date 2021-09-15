from discord.ext import commands

class General (commands.Cog):

    def __init__(self, bot, rcon_run, length_handler):
        self.bot = bot
        self.rcon_run = rcon_run
        self.length_handler = length_handler
        bot.help_command.cog = self
    
    @commands.command(name='players', help='shows the server player list')
    @commands.has_role('Admin')
    async def players(self, ctx):
        response = self.rcon_run('listplayers')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='broadcast', help='sends a message to the server')
    @commands.has_role('Admin')
    async def broadcast(self, ctx, *, message:str):
        response = self.rcon_run(f'broadcast {message}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='console', help='Runs a Conan console command !console <target player> <command> <args>')
    @commands.has_role('Admin')
    async def console(self, ctx, *, command:str,):
        response = self.rcon_run(f'con {command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='rcon', help='Runs a rcon command use clist for a list of rcon commands')
    @commands.has_role('Admin')
    async def rcon(self, ctx, *, command):
        response = self.rcon_run(f'{command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='clist', help='shows the rcon command list')
    @commands.has_role('Admin')
    async def clist(self, ctx):
        response = self.rcon_run('help')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)