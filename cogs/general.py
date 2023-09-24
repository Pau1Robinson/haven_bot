import discord
import asyncio
from discord.ext import commands

from models import Playerlist

class General (commands.Cog):

    def __init__(self, bot, rcon_run, length_handler, add_players_db):
        self.bot = bot
        self.rcon_run = rcon_run
        self.length_handler = length_handler
        self.add_players_db = add_players_db
        self.player_lists_run = True
        bot.help_command.cog = self
    
    # make the player steamids a link to their profile?
    @commands.command(name='players', help='shows the server player list')
    @commands.has_role('Admin')
    async def players(self, ctx):
        response = self.rcon_run('listplayers', ctx,)
        self.add_players_db(response)
        # response_text = self.steam_embedder(response_text)
        # embed = discord.Embed()
        # embed.description = response_text
        # await ctx.channel.send(embed=embed)
        await self.length_handler(response, ctx.channel)
    
    @commands.command(name='playerlist', help='shows an auto updating player list')
    @commands.has_role('Admin')
    async def playerlist(self, ctx):
        self.player_lists_run = True
        previous_list = ''
        playerlist = Playerlist(channel_id=ctx.channel.id, server=ctx.guild.name, user=ctx.author.display_name)
        playerlist.save()
        print(f'!{ctx.invoked_with} Ran:playerlist User:{ctx.author.display_name}#{ctx.author.discriminator} Server:{ctx.guild.name}')
        while self.player_lists_run == True:
            response = self.rcon_run('listplayers', ctx, log=False)
            if response != 'RCON returned an empty response': 
                self.add_players_db(response)   
                await self.length_handler(response, ctx.channel, delete_time=60)
                previous_list = response
            else:
                await self.length_handler(f'{response} \n{previous_list}', ctx.channel, delete_time=60)
            await asyncio.sleep(60)
            
    @commands.command(name='stoplists', help='stop all repeating playerlists')
    @commands.has_role('Admin')
    async def stop_playerlists(self, ctx):
        self.player_lists_run = False
        response = 'stopped all running playerlists'
        await self.length_handler(response, ctx.channel)
    
    @commands.command(name='broadcast', help='sends a message to the server')
    @commands.has_role('Admin')
    async def broadcast(self, ctx, *, message:str):
        response = self.rcon_run(f'broadcast {message}', ctx)
        await self.length_handler(response, ctx.channel)

    @commands.command(name='kick', help='kicks player from the server format !ban <identifier type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def kick(self, ctx, *, command:str):
        response = self.rcon_run(f'kickplayer {command}', ctx,)
        await self.length_handler(response, ctx.channel)
    
    @commands.command(name='ban', help='bans player from the server format !ban <identifier type(index|name|userid|platformid|player)> <player> <message>')
    @commands.has_role('Admin')
    async def ban(self, ctx, *, command:str=''):
        response = self.rcon_run(f'Banplayer {command}', ctx)
        await self.length_handler(response, ctx.channel)
    
    @commands.command(name='unban', help='unbans player from the server format !ban <userid/steamid>')
    @commands.has_role('Admin')
    async def unban(self, ctx, *, player:str):
        response = self.rcon_run(f'unbanplayer {player}', ctx)
        await self.length_handler(response, ctx.channel)
    
    @commands.command(name='banlist', help='shows the server ban list')
    @commands.has_role('Admin')
    async def banlist(self, ctx):
        response = self.rcon_run('listbans', ctx)
        await self.length_handler(response, ctx.channel)
    
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
