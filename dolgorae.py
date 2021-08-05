from itertools import starmap
import discord
import os
from discord.ext.commands import context
from discord.ext.commands.converter import MemberConverter
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from requests.models import default_hooks
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from dpyConsole import Console
import asyncio
import champlist
import random
import mysql.connector
import voice_channel_title

# Main things to setup
TOKEN = 'ODQ1MzAyMjYzMDY0ODIxODIw.YKe_FA.l8nSxnfP2JsVXbKcf7InLZuqtmk'
api_key = 'RGAPI-e55353ae-6344-491c-82a5-0e8e543c1118'
bot = commands.Bot(command_prefix='!',
                   activity=discord.Game(name='add dolphin#0001 for info'))

watcher = LolWatcher(api_key)
league_version = "11.15.1"
my_console = Console(bot)

cnx = mysql.connector.connect(user='customer_191892_dolgoraebot', password = 'Dolphincum0716!',
                              host='na01-sql.pebblehost.com', database = 'customer_191892_dolgoraebot')
db = cnx.cursor()
cnx.autocommit = True

DiscordComponents(bot)

# { 내꺼
#     "id": "AXh6lKaII9YSZ5kA1-6dPs4WUTA8M0ftCvdyf0j74xgGfBk",
#     "accountId": "6M2h1SyvGIsnQ8fwQe1yXdzV9FwTAjQQDX1bnXhin0NAck0",
#     "puuid": "ZZLgSUc6W5wBXvHxtmKy6I-pcCaefoNMB3whg_gouzWdis24Sd7kxRQdMrhGDQ6jW676_PeXjJVDjw",
#     "name": "dolgorae",
#     "profileIconId": 980,
#     "revisionDate": 1622993429000,
#     "summonerLevel": 172
# }


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command()
    async def recent(self, ctx, *, arg: str):
             # collecting data from riot API
        arg = arg.replace(" ", "")
        # print(arg)
        summoner = watcher.summoner.by_name('na1', arg)
        stats = watcher.league.by_summoner('na1', summoner['id'])

        summoner_name = summoner['name']
        print(stats)
        print(summoner)

        try: 
            soloq_recent = watcher.match.matchlist_by_account('NA1', summoner['accountId'], 420,
                                                        None, None, 0, 10, None, None)
        except ApiError:
            print("probably no ranekd games played")
        
        print(soloq_recent)
        str1 = "``" + summoner_name + "'s Recent 10 Matches:``"
        str = ""

        for i in soloq_recent['matches']:
            game_id = i['gameId']
            champ_id = i['champion']
            game = watcher.match.by_id('NA1', game_id)
            
            for j in game['participants']:
                if j['championId'] == champ_id:
                    if j['stats']['win'] == True:
                        str += ":blue_circle: "
                    else:
                        str += ":red_circle: "
                    break
        

        await ctx.channel.send(str1)     
        await ctx.channel.send(str)            

    # Looks up recent 10 soloq games and displays win/loss as emotes
    @commands.command()
    async def search(self, ctx, *, arg: str):
            # collecting data from riot API
        arg = arg.replace(" ", "")
        # print(arg)
        summoner = watcher.summoner.by_name('na1', arg)
        stats = watcher.league.by_summoner('na1', summoner['id'])

        # finding the soloq stats in the 2D array
        queue_count = len(stats)
        flex_pos = -1
        soloq_pos = -1
        for i in range(queue_count):
            if stats[i]['queueType'] == "RANKED_SOLO_5x5":
                soloq_pos = i
            elif stats[i]['queueType'] == "RANKED_FLEX_SR":
                flex_pos = i

        print(stats)
        print(summoner)

        # formatting the URL link
        url_link = "https://na.op.gg/summoner/userName=" + summoner['name']
        url_link = url_link.replace(" ", "+")

        if soloq_pos == -1:
            soloq_page = discord.Embed(
                description="This user is yet to be ranked in solo queue!", color=0xD2C7FF)
        else:
            soloq_page = discord.Embed(color=0xD2C7FF)

            soloq_page.add_field(name="Solo Queue Tier", value=stats[soloq_pos]['tier'] + " " + stats[soloq_pos]['rank'] + " "
                                + str(stats[soloq_pos]['leaguePoints']) + "LP", inline=False)

            soloq_wins = stats[soloq_pos]['wins']
            soloq_losses = stats[soloq_pos]['losses']
            soloq_winrate = soloq_wins/(soloq_wins+soloq_losses)*100
            soloq_page.add_field(name="Wins", value=str(soloq_wins), inline=True)
            soloq_page.add_field(
                name="Losses", value=str(soloq_losses), inline=True)
            soloq_page.add_field(name="Winrate", value="{percentage:.0f}%".format(
                percentage=soloq_winrate), inline=True)

        if flex_pos == -1:
            flex_page = discord.Embed(
                description="This user is yet to be ranked in flex queue!", color=0xffec80)
        else:
            flex_page = discord.Embed(color=0xffec80)

            flex_page.add_field(name="Flex Queue Tier", value=stats[flex_pos]['tier'] + " " + stats[flex_pos]['rank'] + " "
                                + str(stats[flex_pos]['leaguePoints']) + "LP", inline=False)

            flexq_wins = stats[flex_pos]['wins']
            flexq_losses = stats[flex_pos]['losses']
            flexq_winrate = flexq_wins/(flexq_wins+flexq_losses)*100
            flex_page.add_field(name="Wins", value=str(flexq_wins), inline=True)
            flex_page.add_field(name="Losses", value=str(
                flexq_losses), inline=True)
            flex_page.add_field(name="Winrate", value="{percentage:.0f}%".format(
                percentage=flexq_winrate), inline=True)

        # summoner icon link set up
        summoner_icon_link = "http://ddragon.leagueoflegends.com/cdn/" + \
            league_version + "/img/profileicon/" + \
            str(summoner['profileIconId']) + ".png"

        soloq_page.set_author(name=summoner['name'],
                                url=url_link, icon_url=summoner_icon_link)
        flex_page.set_author(name=summoner['name'],
                            url=url_link, icon_url=summoner_icon_link)
        champlist_id = champlist.champlist_by_id()

        try: 
            soloq_recent = watcher.match.matchlist_by_account('NA1', summoner['accountId'], 420,
                                                        None, None, 0, 1, None, None)

            flex_recent = watcher.match.matchlist_by_account('NA1', summoner['accountId'], 440,
                                                            None, None, 0, 1, None, None)
        except ApiError:
            print("probably no ranekd games played")
        else:   
            # champ name, KDA, Win/Lose, CS, match time
            soloq_recent_gameId = soloq_recent["matches"][0]["gameId"]
            soloq_recent_match = watcher.match.by_id('NA1', soloq_recent_gameId)
            
            
            flex_recent_gameId = flex_recent["matches"][0]["gameId"]
            flex_recent_match = watcher.match.by_id('NA1', flex_recent_gameId)
            
            print(summoner['accountId'])
            for y in soloq_recent_match["participantIdentities"]:
                
                if y["player"]["currentAccountId"] == summoner['accountId']:
                    sparticipant_ID = y["participantId"]

            for q in flex_recent_match["participantIdentities"]:
                
                if q["player"]["currentAccountId"] == summoner['accountId']:
                    fparticipant_ID = q["participantId"]

            for z in soloq_recent_match["participants"]:
                if z["participantId"] == sparticipant_ID:
                    s_result = z["stats"]["win"]
                    skills = z["stats"]["kills"]
                    sdeaths = z["stats"]["deaths"]
                    sassists = z["stats"]["assists"]

            for w in flex_recent_match["participants"]:
                if w["participantId"] == fparticipant_ID:
                    f_result = w["stats"]["win"]
                    fkills = w["stats"]["kills"]
                    fdeaths = w["stats"]["deaths"]
                    fassists = w["stats"]["assists"]

            soloq_recent_champId = soloq_recent["matches"][0]["champion"]
            soloq_champion_name = champlist_id[soloq_recent_champId]
            soloq_champ_icon_link = "http://ddragon.leagueoflegends.com/cdn/" + \
                league_version + "/img/champion/" + soloq_champion_name + ".png"

            flex_recent_champId = flex_recent["matches"][0]["champion"]
            flex_champion_name = champlist_id[flex_recent_champId]
            flex_champ_icon_link = "http://ddragon.leagueoflegends.com/cdn/" + \
                league_version + "/img/champion/" + flex_champion_name + ".png"
            
            if f_result == False:
                f_result_str = "Loss"
            else:
                f_result_str = "Win"

            if s_result == False:
                s_result_str = "Loss"
            else:
                s_result_str = "Win"

            # FooterString = "Requested by " + ctx.message.author.name + "#" + ctx.message.author.discriminator
            s_FooterString = "Most recent game: " + s_result_str + " as " + soloq_champion_name + \
                " (" + str(skills) + "/" + str(sdeaths) + "/" + str(sassists) + ")"
            f_FooterString = "Most recent game: " + f_result_str + " as " + flex_champion_name + \
                " (" + str(fkills) + "/" + str(fdeaths) + "/" + str(fassists) + ")"
            soloq_page.set_footer(text=s_FooterString, icon_url=soloq_champ_icon_link)
            flex_page.set_footer(text=f_FooterString, icon_url=flex_champ_icon_link)


        pages = [soloq_page, flex_page]
        message = await ctx.send(embed=pages[0])

        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author

        current_page = 0

        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.clear_reactions()
            else:
                prev_page = current_page

                if str(reaction) == '⬅️':
                    if current_page == 1:
                        current_page = 0

                elif str(reaction) == '➡️':
                    if current_page == 0:
                        current_page = 1

                if current_page != prev_page:
                    await message.edit(embed=pages[current_page])

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
        
class SexCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None        
  
    @commands.command()
    async def sex(self, ctx):
        # select all the rows from existing table, then choose a random integer
        stmt = "select phrase from `sex`"
        db.execute(stmt)
        result = db.fetchall()
        total_rows = len(result)
        print("total rows from select: " +  str(total_rows))
        rand_int = random.randint(0, total_rows - 1)
        print("random integer generated: " + str(rand_int))
        msg = result[rand_int][0]
        await ctx.channel.send(msg)
        
    # @commands.command()
    # async def add_sex(self, ctx, *, arg):
    #     userid = ctx.author.id
    #     try:
    #         stmt = "INSERT INTO `sex` (`userid`, `id`, `phrase`) VALUES ({}, NULL, '{}');".format(userid, arg)
    #         db.execute(stmt)
    #         cnx.commit()
    #         msg = "Phrase successfully inserted for command ``sex``"
    #         await ctx.channel.send(msg)
    #     except mysql.connector.Error as err:
    #         msg = "``Oops, something went wrong: {}``".format(err.message)
    #         await ctx.channel.send(msg)

    @commands.command()
    async def list_sex(self, ctx):
        guildid = ctx.guild.id
        guild = bot.get_guild(guildid)
        try:
            stmt = "select * from sex order by `id` desc"
            db.execute(stmt)
            result = db.fetchall()
            total_rows = len(result)
            pages_needed = total_rows // 5
            pages_needed2 = pages_needed
            extra_lines = total_rows % 5
            
            embedpages = []
            curr = 1
            while pages_needed > 0:
                current_list = 0
                embed=discord.Embed(title="Command List - 'sex'", description="Page {}".format(curr), color=0xf5b2d6)
                embed.set_footer(text="Add dolphin#0001 for more info!")
                while current_list < 5:
                    name = result[total_rows - 1][2]
                    userobj = await bot.fetch_user(result[total_rows - 1][0])
                    username = userobj.name
                    value = "Inserted by {}".format(username)
                    embed.add_field(name=name, value=value, inline=False)
                    current_list += 1
                    total_rows -= 1
                embedpages.append(embed)
                pages_needed -= 1
                curr += 1
            lastembed=discord.Embed(title="Command List - 'sex'", description="Page {}".format(pages_needed2+1), color=0xf5b2d6)
            lastembed.set_footer(text="Add dolphin#0001 for more info!")    
            
            while extra_lines > 0:
                    name = result[extra_lines - 1][2]
                    userobj = await bot.fetch_user(result[extra_lines - 1][0])
                    username = userobj.name
                    value = "Inserted by {}".format(username)
                    lastembed.add_field(name=name, value=value, inline=False)
                    extra_lines -= 1
            embedpages.append(lastembed)   
            
        except mysql.connector.Error as err:
            print(err)
            
        #Sets a default embed
        current = 0
        #Sending first message
        #I used ctx.reply, you can use simply send as well
        mainMessage = await ctx.reply(
            embed = embedpages[current],
            components = [ #Use any button style you wish to :)
                [
                    Button(
                        label = "Prev",
                        id = "back",
                        style = ButtonStyle.blue
                    ),
                    Button(
                        label = f"Page {int(embedpages.index(embedpages[current])) + 1}/{len(embedpages)}",
                        id = "cur",
                        style = ButtonStyle.grey,
                        disabled = True
                    ),
                    Button(
                        label = "Next",
                        id = "front",
                        style = ButtonStyle.blue
                    )
                ]
            ]
        )
        #Infinite loop
        while True:
            #Try and except blocks to catch timeout and break
            try:
                interaction = await bot.wait_for(
                    "button_click",
                    check = lambda i: i.component.id in ["back", "front"], #You can add more
                    timeout = 20.0 #10 seconds of inactivity
                )
                #Getting the right list index
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                #If its out of index, go back to start / end
                if current == len(embedpages):
                    current = 0
                elif current < 0:
                    current = len(embedpages) - 1

                #Edit to new page + the center counter changes
                await interaction.respond(
                    type = InteractionType.UpdateMessage,
                    embed = embedpages[current],
                    components = [ #Use any button style you wish to :)
                        [
                            Button(
                                label = "Prev",
                                id = "back",
                                style = ButtonStyle.blue
                            ),
                            Button(
                                label = f"Page {int(embedpages.index(embedpages[current])) + 1}/{len(embedpages)}",
                                id = "cur",
                                style = ButtonStyle.grey,
                                disabled = True
                            ),
                            Button(
                                label = "Next",
                                id = "front",
                                style = ButtonStyle.blue
                            )
                        ]
                    ]
                )
            except asyncio.TimeoutError:
                #Disable and get outta here
                await mainMessage.edit(
                    components = [
                        [
                            Button(
                                label = "Prev",
                                id = "back",
                                style = ButtonStyle.red,
                                disabled = True
                            ),
                            Button(
                                label = f"Page {int(embedpages.index(embedpages[current])) + 1}/{len(embedpages)}",
                                id = "cur",
                                style = ButtonStyle.grey,
                                disabled = True
                            ),
                            Button(
                                label = "Next",
                                id = "front",
                                style = ButtonStyle.red,
                                disabled = True
                            )
                        ]
                    ]
                )
                break
    
class LeagueAccountAuthentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def success_embed(self, result):
        str1 = result + " 는 이미 씨큐디코내 연동된 롤 계정이에요..."
        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0x8e7cc3)
        embed.add_field(name="😞 이런이런...", value=str1, inline=False)
        embed.add_field(name="☝️ 혹시 사칭이 의심되시나요?", value="🆘씨큐디코 운영진에게 서둘러 연락주세요🆘", inline=False)
        embed.add_field(name="✌️ 다른 롤 계정으로 연동이 필요하신가요?", value="🔄 새로운 커맨드를 입력해주세요 (**/재인증**) 🔄", inline=False)
        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
        return embed

    def init_success_embed(self, result):
        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0x64d65c)
        str1 = result + "님, 변경된 소환사 아이콘이 확인되었습니다! \n닉네임이 인증된 롤계정와 연동되었으며, 정회원 권한이 부여됩니다! \n씨큐의 일원이 되신걸 환영합니다! 앞으로 더욱 더 친해져봐요!"
        embed.add_field(name="👌 계정 인증성공!", value=str1, inline=False)
        embed.add_field(name="혹시,", value="롤계정 닉네임이 변경되셨나요? 저에게 새로운 커맨드를 입력해주세요! \n(**/업데이트**)", inline=False)
        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
        return embed

    def init_embed(self):  
        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0x8e7cc3)
        embed.add_field(name="씨큐디코와 롤 계정 연동을 위해 커맨드를 입력해주세요!", value=" (/연동 롤닉네임)", inline=False)
        embed.add_field(name="예)/연동 CQ Dolphin", value="커맨드내 실수를 하셨다면, 재인증 커맨드를 입력해주세요! (/재인증)", inline=False)
        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")    
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):    
        if message.author == bot.user:
            return
        

        #obtain the context to work with
        ctx = await bot.get_context(message)
        user_id = message.author.id
        guild = bot.get_guild(427635768844877824)
        member = await guild.fetch_member(user_id)
        dm = member.dm_channel

        str1 = member.name + " says: " + message.content
        print(str1)

        #check if this is a dm received
        if message.channel.id == 872539969397334057 and message.content == "/인증":
                if dm == None:
                    dm = await member.create_dm()
                embed = self.init_embed()
                await dm.send(embed=embed)

        if message.channel.id == 872539969397334057 and not user_id == 426955675592163329:
            await message.delete()

        if isinstance(message.channel, discord.DMChannel):
            if dm == None:
                    dm = await member.create_dm()
                    
            if message.content == "/인증":
                embed = self.init_embed()
                await dm.send(embed=embed)

            # yet to be implemented
            elif message.content == "/업데이트":
                await dm.send('``아직 개발이 되지않은 기능입니다! 조금만 기다려주세요``')

            elif message.content.startswith("/연동 "):
                just_name = message.content[4:]
                just_name1 = just_name.replace(" ", "")
                summoner = watcher.summoner.by_name('NA1', just_name1)
                summonername = summoner["name"]
                summoner_current_icon = summoner["profileIconId"]
                summoner_id = summoner["id"]

                summoner_info = watcher.league.by_summoner('NA1', summoner_id)
                summoner_tier = "UNRANKED"
                for x in summoner_info:
                    if x["queueType"] == "RANKED_SOLO_5x5":
                        summoner_tier = x["tier"]
            
                look_up_summoner = "SELECT * FROM league_acc_authentication where summoner_name = '{}'".format(summonername)
                db.execute(look_up_summoner)
                result = db.fetchall()

                print(result)

                # if the user exists and already authenticated
                if len(result) == 1 and result[0][4] == 1 and result[0][2] == member.id:
                    embed = self.success_embed(result[0][0])
                    await dm.send(embed=embed)

                    new_name = result[0][0] + " 🌟"
                    await member.edit(nick = new_name)

                    #정회원
                    member_role = guild.get_role(683841495417225301)
                    roles = member.roles
                    if member_role not in roles:
                        log_chat = guild.get_channel(870718238173044767)
                        str1 = "Added role **{}** to {} successfully. League name: **{}**".format(member_role.name, member.mention, result[0][0])
                        await member.add_roles(member_role, reason ="League Account connected")
                        await log_chat.send(str1)
                    return

                elif len(result) == 1 and result[0][4] == 1 and not result[0][2] == member.id:
                    log_chat = guild.get_channel(870718238173044767)
                    original_member = await guild.fetch_member(result[0][2])
                    str1 = "**Warning** {} just tried to authenticate with league account already registered by {}! League name: **{}**".format(member.mention, original_member.mention, result[0][0])
                    await log_chat.send(str1)
                    return

                # If this user does not exist yet in the DB, add into DB and also create icon authentication
                elif len(result) == 0:
                    stmt = ("INSERT INTO `league_acc_authentication` (`summoner_name`, `summoner_id`, `discord_id`, `summoner_rank`, `authenticated`)"
                            " VALUES('{}','{}',{},'{}',{})".format(summonername, summoner_id, message.author.id, summoner_tier, 0))
                    db.execute(stmt)
                    cnx.commit()
                    
                    stmt2 = ("INSERT INTO `icon_authentication` (`current`, `required`, `discord_id`, `summoner_id`)" 
                        "VALUES ({}, {}, {}, '{}')".format(summoner_current_icon, 0, message.author.id, summoner_id))
                    db.execute(stmt2)
                    cnx.commit()

                # Now, send the icon prompt. Random icon selected
                random_icon = random.randint(21, 28)
                stmt3 = ("update icon_authentication set required = {} where discord_id = {}").format(random_icon, message.author.id)
                db.execute(stmt3)
                cnx.commit()

                # Just in case the user is using the default icon, we keep choosing a new one
                while random_icon == summoner_current_icon:
                    random_icon = random.randint(21, 28)
                
                random_icon_link = "http://ddragon.leagueoflegends.com/cdn/" + league_version + "/img/profileicon/" + str(random_icon) + ".png"

                embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0x8e7cc3)
                embed.set_thumbnail(url=random_icon_link)
                embed.add_field(name="선생님의 롤계정 소환사 아이콘을 오른쪽의 아이콘으로 변경 후, 확인 커맨드를 입력해주세요!", value="➡️ **/확인**", inline=False)
                embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
                await dm.send(embed=embed)

            elif message.content == "/확인":

                # get the summoner id associated with this discord acocunt
                stmt = "select summoner_id, authenticated, summoner_name from league_acc_authentication where discord_id = {} ".format(message.author.id)
                db.execute(stmt)
                result = db.fetchall()

                summoner_id = result[0][0]
                
                # This user has already been authenticated
                if result[0][1] == 1:
                    user_id = message.author.id
                    guild = bot.get_guild(427635768844877824)
                    member = await guild.fetch_member(user_id)
                    new_name = result[0][2] + " 🌟"
                    await member.edit(nick = new_name)

                    member_role = guild.get_role(683841495417225301)
                    roles = member.roles
                    if member_role not in roles:
                        await member.add_roles(member_role, reason ="League Account connected")
                        log_chat = guild.get_channel(870718238173044767)
                        str1 = "Added role **{}** to {} successfully. League name: **{}**".format(member_role.name, member.mention, result[0][2])
                        await log_chat.send(str1)
                        embed = self.success_embed(result[0][2])
                        await dm.send(embed=embed)

                # If not, go ahead and check
                else:
                    # check if required == random icon
                    summoner_obj = watcher.summoner.by_id('NA1', summoner_id)
                    current_icon = summoner_obj["profileIconId"]
                    print(current_icon)
                    summoner_name = summoner_obj["name"]

                    stmt2 = "select required from icon_authentication where discord_id = '{}'".format(message.author.id)
                    db.execute(stmt2)
                    result2 = db.fetchall()
                    
                    required_icon = result2[0][0]
                    print(required_icon)
                    # authentication successful, change bool on authentication row
                    if current_icon == required_icon:
                        stmt = "update league_acc_authentication set authenticated = 1 where discord_id = {}".format(message.author.id)
                        db.execute(stmt)
                        cnx.commit()
                        
                        embed = self.init_success_embed(summoner_name)
                        await dm.send(embed=embed)
                        
                        # 서버 닉네임 change to summoner name + the icon, assign the rank role as well
                        user_id = message.author.id
                        guild = bot.get_guild(427635768844877824)
                        member = await guild.fetch_member(user_id)
                        new_name = summoner_name + " 🌟"
                        await member.edit(nick = new_name)

                        member_role = guild.get_role(683841495417225301)
                        roles = member.roles
                        if member_role not in roles:
                            log_chat = guild.get_channel(870718238173044767)
                            str1 = "Added role **{}** to {} successfully. League name: **{}**".format(member_role.name, member.mention, result[0][2])
                            await member.add_roles(member_role, reason ="League Account connected")
                            await log_chat.send(str1)
                        
                    # authentication failed
                    else:
                        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0xff5c5c)
                        embed.add_field(name="⛔ 계정 인증실패", value="변경된 소환사 아이콘이 확인되지 않았습니다. \n다시 연동을 실행하시려면 커맨드를 입력해주세요! **(/연동 롤닉네임)**", inline=False)
                        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
                        await ctx.send(embed=embed)

            #3일에 한번씩
            elif message.content == "/재인증":
                stmt = "delete from league_acc_authentication where discord_id = {}".format(message.author.id)
                db.execute(stmt)
                cnx.commit()

                stmt2 = "delete from icon_authentication where discord_id = {}".format(message.author.id)
                db.execute(stmt2)
                cnx.commit()

                await ctx.send('``리셋 완료, 저에게 다시`` **/인증** ``이라고 보내주세요!``')

            else:
                await ctx.send('``앗, 오타가 있어요. 저에게 /인증, /연동 닉네임, /재인증, /업데이트 중 하나를 보내주세요...``')
        




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
    
class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await bot.get_context(message)
        if not isinstance(ctx.channel, discord.DMChannel):
            print(message.author.display_name + " says " + message.content + " in " + message.channel.name)

        if message.author == bot.user:
            return

        if message.content.startswith("@"):
            author_roles = message.author.roles
            found = False

            #check if it's existing role name or not
            existing = False
            server_roles = message.guild.roles
            new_msg = message.content + ' '
            for z in server_roles:
                if new_msg.startswith('@' + z.name + ' '):
                    existing = True
                    role_name = z.name

            if existing:
                for y in author_roles:
                    role_name_with_tag = '@' + y.name + ' '
                    new_msg = message.content + ' '
                    if new_msg.startswith(role_name_with_tag):
                        if y.mentionable:
                            await y.edit(mentionable = False)
                        found = True
                        valo_role = y
                if found:
                # valo_role = discord.utils.get(message.guild.roles, id=role.id)
                    msg_len = len(valo_role.name) + 1
                    substring = message.content[msg_len:]
                    await valo_role.edit(mentionable = True)
                    msg = "**{}** says: {} {}".format(message.author.display_name, valo_role.mention, substring)
                    await message.channel.send(msg)
                    await valo_role.edit(mentionable = False)
                else:
                    warning = "**{}**님, **{}** 역할을 태그할 수 있는 권한이 없습니다.".format(message.author.display_name, role_name)
                    await message.channel.send(warning)
                await message.delete()   

            
        if '누비쿤' in message.content:
            await message.channel.send('``누비쿤 조용히해``')

        if '현수' in message.content:
            await message.channel.send('``플레로 돌아오세요``')

        if '도비' in message.content:
            await message.channel.send('``도비는 자유에요!``:socks:')

        userid = message.author.id
        # bring all the saved counter words of this user

        exclu = message.content.startswith("$add_counter")
        exclu2 = message.content.startswith("$delete_counter")
        if not exclu and not exclu2:        
            bring = "SELECT `word` FROM `counter` WHERE `userid` = {}".format(userid)
            db.execute(bring)
            result = db.fetchall()
            for x in result:
                theword = x[0]
                if theword in message.content:
                    cnt = message.content.count(theword)
                    stmt = "SELECT `count` FROM `counter` WHERE `userid` = {} AND `word` = '{}'".format(userid, theword)
                    db.execute(stmt)
                    result = db.fetchall()
                    countnum = result[0][0]
                    countnum += cnt
                    newstmt = "UPDATE `counter` SET `count` = {} WHERE `userid` = {} AND `word` = '{}'".format(countnum, userid, theword)
                    db.execute(newstmt)
                    cnx.commit()
                    msg = "``{}'s {} counter: {}``".format(message.author.display_name, theword, countnum)
                    await message.channel.send(msg)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        
        # Get the list of temp channels (there's only gonna be 2 or 3)
        stmt = "SELECT channel_ID FROM `temp_channels`"
        db.execute(stmt)
        result = db.fetchall()

        newlist = []
        for x in result:
            newlist.append(x[0])

        create_channels = [865800729653936138, 741783612298625035, 865800959078957096]

        if after.channel is not None:
            if after.channel.id in create_channels:
                channel_to_clone = discord.utils.get(member.guild.voice_channels, id=after.channel.id)

                titles = voice_channel_title.voice_channel_titles()
                rand_int = random.randint(0, len(titles)-1)
                name = titles[rand_int]
                cloned_channel = await channel_to_clone.clone(name=name)
                cloned_channel_id = cloned_channel.id

                sql_statement = "INSERT INTO `temp_channels` (`creater_ID`, `channel_ID`, `channel_name`, `max_user`) VALUES ('{}', '{}', '{}', '{}')".format(member.id, cloned_channel_id, name, after.channel.user_limit)
                db.execute(sql_statement)
                cnx.commit()

                base = discord.utils.get(member.guild.voice_channels, id=493665433723863040)
                category = discord.utils.get(member.guild.categories, id=701586126611284018)
                overwrite = discord.PermissionOverwrite()
                overwrite.manage_channels = True
                await cloned_channel.set_permissions(member, overwrite =overwrite)
                await cloned_channel.move(category=category, before=base)
                await member.move_to(cloned_channel)

        if before.channel is not None:
            if before.channel.id in newlist:
                if not before.channel.members:
                    channel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
                    stmt = "delete from `temp_channels` where `channel_ID` = {}".format(channel.id)
                    db.execute(stmt)
                    cnx.commit()
                    await channel.delete(reason = "No longer in usage")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        guild = bot.get_guild(payload.guild_id)
        user = payload.member
        message_id = payload.message_id
        member_role = guild.get_role(484970709324398604)
        if message_id == 871760325949665330:
            #Added wrong reaction, then delete
            if payload.emoji.id == 847986659790422047:
                roles = user.roles
                if member_role not in roles:
                    await user.add_roles(member_role, reason ="Agreed to the terms")
                    log_chat = guild.get_channel(870718238173044767)
                    str = "Added role **{}** to {} successfully.".format(member_role.name, user.mention)
                    await log_chat.send(str)

            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(871760325949665330)
            await message.remove_reaction(payload.emoji, user)
            #Added the right reaction, then proceed with procedure

            

my_console.start()
bot.add_cog(LeagueCommands(bot))
bot.add_cog(CounterCommands(bot))
bot.add_cog(SexCommands(bot))
bot.add_cog(MainCog(bot))
bot.add_cog(LeagueAccountAuthentication(bot))
bot.run(TOKEN)