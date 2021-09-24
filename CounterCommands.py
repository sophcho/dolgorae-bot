from dotenv import load_dotenv
import discord, os, asyncio, champlist, random, mysql.connector, voice_channel_title, logging, time
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from dpyConsole import Console
import LeagueCommands



cnx = mysql.connector.connect(user=os.getenv("mysql_user"), password =os.getenv("mysql_pw") ,
                              host=os.getenv("mysql_host"), database =os.getenv("mysql_db") )
db = cnx.cursor()
cnx.autocommit = True

class CounterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None    
    
    @commands.command()
    async def add_counter(self, ctx, *arg):
        userid = ctx.author.id
        if len(arg) == 1:
            try:
                word = arg[0]
                stmt =  "insert into counter (userid, word, count) values ({}, '{}', 0)".format(userid, word)
                db.execute(stmt)
                cnx.commit()
                msg = "``Now keeping track of {}'s keyword: {}``".format(ctx.author.display_name, word)
                await ctx.channel.send(msg)
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    msg = "``This keyword is being counted already!``"
                    await ctx.channel.send(msg)
                else:
                    msg = "``Oops, something went wrong: {}".format(err.message)
                    await ctx.channel.send(msg)
        else:
            msg = "``Hey, you must enter a single word as a keyword!``"
            await ctx.channel.send(msg)

    @commands.command()
    async def delete_counter(self, ctx, *arg):
        userid = ctx.author.id
        if len(arg) == 1:
            try:
                word = arg[0]
                check = "select * from counter where userid = {} AND word ='{}'".format(userid, word)
                db.execute(check)
                result = db.fetchone()
                if result == None:
                    msg = "``Hey, this word is not being counted for you!``"
                    await ctx.channel.send(msg)
                else:    
                    stmt =  "delete from counter where userid = {} AND word = '{}'".format(userid, word)
                    db.execute(stmt)
                    cnx.commit()
                    msg = "``Deleted {}'s {} keyword.``".format(ctx.author.display_name, word)
                    await ctx.channel.send(msg)
            except mysql.connector.Error as err:
                    msg = "``Oops, something went wrong: {}".format(err.message)
                    await ctx.channel.send(msg)
        else:
            msg = "``Hey, you must enter a single word as a keyword!``"
            await ctx.channel.send(msg)

    @commands.command()
    async def my_counter(self, ctx):
        userid = ctx.author.id
        try:
            stmt = "select `word` from `counter` where userid = {}".format(userid)
            db.execute(stmt)
            result = db.fetchall()
            msg = "{}'s keywords: ".format(ctx.author.display_name)
            first = True
            for x in result:
                if first:
                    msg = msg + "``" + x[0] + "``"
                    first = False
                else:
                    msg = msg + ", " + "``" + x[0] + "``"
            await ctx.channel.send(msg)
        except mysql.connector.Error as err:
            msg = "``Oops, something went wrong: {}".format(err.message)
            await ctx.channel.send(msg)
            
def setup(bot: commands.Bot):
    bot.add_cog(CounterCommands(bot))