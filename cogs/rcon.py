from discord.ext import commands

class Rcon (commands.Cog):

    def __init__(self, bot, rcon_run, length_handler):
        self.bot = bot
        self.rcon_run = rcon_run
        self.length_handler = length_handler
    
    @commands.command(name='rcon', help='Runs a rcon command use clist for a list of rcon commands')
    @commands.has_role('Admin')
    async def rcon(self, ctx, *, command):
        response = self.rcon_run(ctx, f'{command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='clist', help='shows the rcon command list')
    @commands.has_role('Admin')
    async def clist(self, ctx):
        response = self.rcon_run(ctx, 'help')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='console', help='Runs a Conan console command !console <target player> <command> <args>')
    @commands.has_role('Admin')
    async def console(self, ctx, *, command:str,):
        response = self.rcon_run(ctx, f'con {command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
