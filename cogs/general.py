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
        response = self.rcon_run(ctx, 'listplayers')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='broadcast', help='sends a message to the server')
    @commands.has_role('Admin')
    async def broadcast(self, ctx, *, message:str):
        response = self.rcon_run(ctx, f'broadcast {message}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)

    @commands.command(name='kick', help='kicks player from the server format !ban <identifer type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def kick(self, ctx, *, command:str):
        response = self.rcon_run(ctx, f'kickplayer {command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='ban', help='bans player from the server format !ban <identifer type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def ban(self, ctx, *, command:str=''):
        response = self.rcon_run(ctx, f'Banplayer {command}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='unban', help='unbans player from the server format !ban <userid/steamid>')
    @commands.has_role('Admin')
    async def unban(self, ctx, *, player:str):
        response = self.rcon_run(ctx, f'unbanplayer {player}')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='banlist', help='shows the server ban list')
    @commands.has_role('Admin')
    async def banlist(self, ctx):
        response = self.rcon_run(ctx, 'listbans')
        response_text = response.body.decode("utf-8")
        await self.length_handler(response_text, ctx)
