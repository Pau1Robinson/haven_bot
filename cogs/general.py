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
        # response_text = self.steam_embedder(response_text)
        # embed = discord.Embed()
        # embed.description = response_text
        # await ctx.channel.send(embed=embed)
        await self.length_handler(response, ctx)
    
    @commands.command(name='playerlist', help='shows an auto updating player list')
    @commands.has_role('Admin')
    async def playerlist(self, ctx):
        self.player_lists_run = True
        previous_list = ''
        print(f'!{ctx.invoked_with} Ran:playerlist User:{ctx.author.display_name}#{ctx.author.discriminator} Server:{ctx.guild.name}')
        while self.player_lists_run == True:
            response = self.rcon_run(ctx, 'listplayers', log=False)
            if response != 'RCON returned an empty response':    
                await self.length_handler(response, ctx, delete_time=60)
                previous_list = response
            else:
                await self.length_handler(f'{response} \n{previous_list}', ctx, delete_time=60)
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
        await self.length_handler(response, ctx)

    @commands.command(name='kick', help='kicks player from the server format !ban <identifier type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def kick(self, ctx, *, command:str):
        response = self.rcon_run(ctx, f'kickplayer {command}')
        await self.length_handler(response, ctx)
    
    @commands.command(name='ban', help='bans player from the server format !ban <identifier type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def ban(self, ctx, *, command:str=''):
        response = self.rcon_run(ctx, f'Banplayer {command}')
        await self.length_handler(response, ctx)
    
    @commands.command(name='unban', help='unbans player from the server format !ban <userid/steamid>')
    @commands.has_role('Admin')
    async def unban(self, ctx, *, player:str):
        response = self.rcon_run(ctx, f'unbanplayer {player}')
        await self.length_handler(response, ctx)
    
    @commands.command(name='banlist', help='shows the server ban list')
    @commands.has_role('Admin')
    async def banlist(self, ctx):
        response = self.rcon_run(ctx, 'listbans')
        await self.length_handler(response, ctx)
    
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
