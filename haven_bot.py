import os
import valve.rcon

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ADDRESS = (os.getenv('SERVER_IP'), int(os.getenv('RCON_PORT')))
PASSWORD = os.getenv('RCON_PASSWORD')

bot = commands.Bot(command_prefix='!')
#add command catagories

@bot.command(name='clist', help='shows the rcon command list')
@commands.has_role('Admin')
async def clist(ctx):
    response = rcon_run('help')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='players', help='shows the server player list')
@commands.has_role('Admin')
async def list_players(ctx):
    response = rcon_run('listplayers')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='placeables', help='shows a list of each clans placeables')
@commands.has_role('Admin')
async def clan_placeables(ctx):
    response = rcon_run(sql_run('placeables'))
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='buildings', help='shows a list of each clans building pieces')
@commands.has_role('Admin')
async def clan_buildings(ctx):
    response = rcon_run(sql_run('buildings'))
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='blocks', help='shows a list of single block foundations')
@commands.has_role('Admin')
async def clan_buildings(ctx):
    response = rcon_run(sql_run('blocks'))
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='chars', help='shows a list of all characters')
@commands.has_role('Admin')
async def clan_buildings(ctx):
    response = rcon_run(sql_run('chars'))
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='banlist', help='shows the server ban list')
@commands.has_role('Admin')
async def list_bans(ctx):
    response = rcon_run('listbans')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='broadcast', help='sends a message to the server')
@commands.has_role('Admin')
async def list_bans(ctx, *, message:str):
    response = rcon_run(f'broadcast {message}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='ban', help='bans player from the server format !ban <identifer type(index|name|userid|platformid|player)> <player> <message>')
@commands.has_role('Admin')
async def list_bans(ctx, identifier:str, player:str, *, message:str=''):
    response = rcon_run(f'Banplayer {identifier} {player} {message}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='unban', help='unbans player from the server format !ban <userid/steamid>')
@commands.has_role('Admin')
async def list_bans(ctx, player:str):
    response = rcon_run(f'unbanplayer {player}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='kick', help='kicks player from the server format !ban <identifer type(index|name|userid|platformid|player)> <player> <message>')
@commands.has_role('Admin')
async def list_bans(ctx, identifier:str, player:str, *, message:str=''):
    response = rcon_run(f'kickplayer {identifier} {player} {message}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='console', help='Runs a Conan console command !console <target player> <command> <args>')
@commands.has_role('Admin')
async def list_bans(ctx, player:str, command:str, *, args:str=''):
    response = rcon_run(f'con {player} {command} {args}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

@bot.command(name='rcon', help='Runs a rcon command use clist for a list of rcon commands')
@commands.has_role('Admin')
async def list_bans(ctx, *, command):
    response = rcon_run(f'{command}')
    response_text = response.body.decode("utf-8")
    await length_handler(response_text, ctx)

async def length_handler(message, ctx):
    while len(message) > 1900:
        split = message.rfind('\n', 0, 1900)
        await ctx.channel.send(f'```{message[0:split+1]}```')
        message = message[split:len(message)]
    await ctx.channel.send(f'```{message}```')

def rcon_run(command):
    #add disconnetion to address timeout issue?
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
    return response

def sql_run(command):
    sql_file = open(f'sql/{command}.sql')
    sql_string = sql_file.read()
    sql_file.close()
    return f'sql {sql_string}'

print('Haven bot online')
bot.run(TOKEN)