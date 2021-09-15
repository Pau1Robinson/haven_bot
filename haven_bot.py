import os
import valve.rcon

from discord.ext import commands
from dotenv import load_dotenv

from cogs.general import  General
from cogs.queries import Queries
from cogs.admin import Admin

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ADDRESS = (os.getenv('SERVER_IP'), int(os.getenv('RCON_PORT')))
PASSWORD = os.getenv('RCON_PASSWORD')

bot = commands.Bot(command_prefix='!')

async def length_handler(message, ctx):
    while len(message) > 1900:
        split = message.rfind('\n', 0, 1900)
        await ctx.channel.send(f'```{message[0:split+1]}```')
        message = message[split:len(message)]
    await ctx.channel.send(f'```{message}```')

def rcon_run(command):
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

bot.add_cog(General(bot, rcon_run, length_handler))
bot.add_cog(Queries(bot, rcon_run, length_handler))
bot.add_cog(Admin(bot, rcon_run, length_handler))

print('Haven bot online')
bot.run(TOKEN)