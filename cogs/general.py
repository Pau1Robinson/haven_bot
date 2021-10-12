import discord
import asyncio
from discord.ext import commands

class General (commands.Cog):

    def __init__(self, bot, rcon_run, length_handler):
        self.bot = bot
        self.rcon_run = rcon_run
        self.length_handler = length_handler
        self.player_lists_run = True
        bot.help_command.cog = self
    
    # make the player steamids a link to their profile?
    @commands.command(name='players', help='shows the server player list')
    @commands.has_role('Admin')
    async def players(self, ctx):
        response = self.rcon_run(ctx, 'listplayers')
        response_text = response.body.decode("utf-8")
        # response_text = self.steam_embedder(response_text)
        # embed = discord.Embed()
        # embed.description = response_text
        # await ctx.channel.send(embed=embed)
        await self.length_handler(response_text, ctx)
    
    @commands.command(name='playerlist', help='shows a auto updating player list')
    @commands.has_role('Admin')
    async def playerlist(self, ctx):
        self.player_lists_run = True
        while self.player_lists_run == True:
            response = self.rcon_run(ctx, 'listplayers')
            response_text = response.body.decode("utf-8")
            await self.length_handler(response_text, ctx, delete_time=60)
            await asyncio.sleep(60)

    @commands.command(name='stoplists', help='stop all repeating playerlists')
    @commands.has_role('Admin')
    async def stop_playerlists(self, ctx):
        self.player_lists_run = False
        response = 'stopped all running playerlists'
        await self.length_handler(response, ctx)
    
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
    
    def steam_embedder(self, message):
        #changes playerlist steam id's into steamlinks
        #discord currently doesn't allow embeds in this way
        list = message.split('|')
        for i, string in enumerate(list):
            if string.find('Steam') == True:
                string = list[i-1]
                string = string.strip()
                string = f' [{string}](\'https://steamcommunity.com/profiles/{string}/\') '
                list[i-1] = string
        message = ' '.join(list)
        return message

class PlayerList():

    def __init__(self, rcon_run, ctx):
        player_list = ""
        ctx = self.ctx
        rcon_run = self.rcon_run
    
    def get_players(self):
        response = self.rcon_run(self.ctx, 'listplayers')
        response_text = response.body.decode("utf-8")
        return response_text

    def length_list(self, message):
        message_list = []
        while len(message) > 1900:
            split = message.rfind('\n', 0, 1900)
            message_list.append(f'```{message[0:split+1]}```')
            message = message[split:len(message)]
        message_list.append(f'```{message}```')
        return message_list

