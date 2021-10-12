from discord.ext import commands

class Queries (commands.Cog):

    def __init__(self, bot, rcon_run, length_handler):
        self.bot = bot
        self.rcon_run = rcon_run
        self.length_handler = length_handler
    
    def sql_run(self, command):
        sql_file = open(f'sql/{command}.sql')
        sql_string = sql_file.read()
        sql_file.close()
        return f'sql {sql_string}'

    @commands.command(name='buildings', help='shows a list of each clans building pieces')
    @commands.has_role('Admin')
    async def buildings(self, ctx):
        response = self.rcon_run(ctx, self.sql_run('buildings'))
        await self.length_handler(response, ctx)
    
    @commands.command(name='placeables', help='shows a list of each clans placeables')
    @commands.has_role('Admin')
    async def placeables(self, ctx):
        response = self.rcon_run(ctx, self.sql_run('placeables'))
        await self.length_handler(response, ctx)
    
    @commands.command(name='blocks', help='shows a list of single block foundations')
    @commands.has_role('Admin')
    async def blocks(self, ctx):
        response = self.rcon_run(ctx, self.sql_run('blocks'))
        await self.length_handler(response, ctx)
    
    @commands.command(name='chars', help='shows a list of all characters')
    @commands.has_role('Admin')
    async def chars(self, ctx):
        response = self.rcon_run(ctx, self.sql_run('chars'))
        await self.length_handler(response, ctx)