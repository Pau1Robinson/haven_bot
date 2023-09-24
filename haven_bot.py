import os
import valve.rcon
import discord
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv
from mongoengine import connect

from cogs.general import  General
from cogs.queries import Queries
from cogs.rcon import Rcon

from models import Playerlist
from models import Player

load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
DB_URI = os.getenv('DB_URI')

ADDRESS = (os.getenv('SERVER_IP'), int(os.getenv('RCON_PORT')))
PASSWORD = os.getenv('RCON_PASSWORD')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

async def length_handler(message, channel, delete_time=None):
    while len(message) > 1900:
        split = message.rfind('\n', 0, 1900)
        await channel.send(f'```{message[0:split+1]}```', delete_after=delete_time)
        message = message[split:len(message)]
    await channel.send(f'```{message}```', delete_after=delete_time)

def rcon_run(command, ctx=False, log=True):
    if ctx and log:
        print(f'!{ctx.invoked_with} Ran:{command[0 : 25]} User:{ctx.author.display_name}#{ctx.author.discriminator} Server:{ctx.guild.name}')
    try:
        rcon = valve.rcon.RCON(ADDRESS, PASSWORD)
        rcon.connect()
        rcon.authenticate()
        response = rcon.execute(command)
    except valve.rcon.RCONCommunicationError:
        response = 'rcon connection failed'
    except valve.rcon.RCONError:
        response = 'rcon connection failed'
    except valve.rcon.RCONAuthenticationError:
        response = 'rcon authentication failed'
    except ConnectionRefusedError:
        response = 'rcon connection refused'
    if hasattr(response, 'body'):
        response_text = response.body.decode("utf-8")
        return response_text
    else:
        return 'RCON returned an empty response'
    
async def main():
    print('Haven bot online')

    async with bot:
        await bot.add_cog(General(bot, rcon_run, length_handler, add_players_db))
        await bot.add_cog(Queries(bot, rcon_run, length_handler))
        await bot.add_cog(Rcon(bot, rcon_run, length_handler))
        await bot.start(TOKEN)      

async def run_playerlist(channel):
    channel = await bot.fetch_channel(channel)
    previous_list = ''
    player_lists_run = True
    while player_lists_run == True:
        response = rcon_run('listplayers', ctx=False, log=False)
        if response != 'RCON returned an empty response':
            add_players_db(response)
            await length_handler(response, channel, delete_time=60)
            previous_list = response
        else:
            await length_handler(f'{response} \n{previous_list}', channel, delete_time=60)
        await asyncio.sleep(60)

def add_players_db(response):
    response = response.splitlines()
    if len(response) > 1:
        for response_player in response[1:]:
            response_player = response_player.split('|')
            if not Player.objects(server_id=response_player[3]):
                player = Player(char_name=response_player[1],funcom_id=response_player[2],server_id=response_player[3],platform_id=response_player[4],platform_name=response_player[5])
                player.save()
                print(f'added player {response_player[2]} to DB')

@bot.event
async def on_ready():
    for playerlist in Playerlist.objects:
        print(f'Starting Playerlist from Server:{playerlist.server} started by user:{playerlist.user}')
        await run_playerlist(playerlist.channel_id)

connect(host=DB_URI)
asyncio.run(main())


