from dotenv import load_dotenv
import discord, os, random, mysql.connector, logging
from discord_components import DiscordComponents
from riotwatcher import LolWatcher
from discord.ext import commands
from dpyConsole import Console

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Main things to setup
load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

my_console = Console(bot)
DiscordComponents(bot)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='여러분의 의견을'))


@bot.command()
async def repeat(ctx, *, arg):
    await ctx.channel.send(arg)
  
@bot.command()
async def mute(ctx, member: discord.Member):
    print("in the function")
    perms = ctx.channel.overwrites_for(member)
    perms.send_messages = False
    await ctx.channel.set_permissions(member, overwrite=perms)
    await ctx.channel.send("muted")

@bot.command()
async def 가위바위보(ctx, member1: discord.Member, member2: discord.Member):
    mem1num = random.randint(0, 2)
    mem2num = random.randint(0, 2)
    result = [":v:", ":hand_splayed:", ":fist:"]
    # 가위 보 바위
    draw = False
    mem1win = False
    
    if mem1num == mem2num:
        draw = True
    
    if draw == False:
        if mem1num == 0:
            if mem2num == 1:
                mem1win = True
            elif mem2num == 2:
                mem1win = False
        elif mem1num == 1:
            if mem2num == 0:
                mem1win = False
            elif mem2num == 2:
                mem1win = True
        else:
            if mem2num == 0:
                mem1win = True
            elif mem2num == 1:
                mem1win = False
    
    if mem1win:
        premsg = "``{}:`` " + result[mem1num] + "\n``{}:`` " + result[mem2num] + "\n``The winner is:`` {}!"
        msg = premsg.format(
            member1.display_name, member2.display_name, member1.mention)
    elif draw:
        premsg = "``{}:`` " + result[mem1num] + "\n``{}:`` " + result[mem2num] + "\n``Draw -- play again by clicking the`` :star: ``reaction``"
        msg = premsg.format(
            member1.display_name, member2.display_name)
        
    else:
        premsg = "``{}:`` " + result[mem1num] + "\n``{}:`` " + result[mem2num] + "\n``The winner is:`` {}!"
        msg = premsg.format(
            member1.display_name, member2.display_name, member2.mention)
        
    final = await ctx.channel.send(msg)
    # if draw:
    #     await final.add_reaction('⭐')
        
    #     while True:
    #         try:
    #             reaction, user = await bot.wait_for('reaction_add', timeout=10.0)
    #            # await final.remove_reaction(reaction, user)
    #         except asyncio.TimeoutError:
    #             await final.clear_reactions()
    #         else:
    #             await ctx.invoke(bot.get_command('가위바위보'), member1 = member1, member2 = member2)
    #             await final.clear_reactions()

@my_console.command()
async def send_msg(arg):
    channel = bot.get_channel(432756157497475092)
    await channel.send(arg)
    
my_console.start()

bot.load_extension("CounterCommands")
bot.load_extension("LeagueCommands")
bot.load_extension("LeagueAccountAuthentication")
bot.load_extension("SexCommands")
bot.load_extension("MainCog")

bot.run(TOKEN)