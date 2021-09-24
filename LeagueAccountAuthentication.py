from dotenv import load_dotenv
import discord, os, asyncio, champlist, random, mysql.connector, voice_channel_title, logging, time
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from dpyConsole import Console

load_dotenv('.env')
api_key = os.getenv("api_key")

cnx = mysql.connector.connect(user=os.getenv("mysql_user"), password =os.getenv("mysql_pw") ,
                              host=os.getenv("mysql_host"), database =os.getenv("mysql_db") )
db = cnx.cursor()
cnx.autocommit = True

watcher = LolWatcher(api_key)
league_version = "11.15.1"

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
        str1 = "💎 " + result + "님, 변경된 소환사 아이콘이 확인되었습니다! \n💎 닉네임이 인증된 롤계정와 연동되었으며, 정회원 권한이 부여됩니다! \n\n👪 씨큐의 일원이 되신걸 환영합니다! 앞으로 더욱 더 친해져봐요!"
        embed.add_field(name="👌 계정 인증성공!", value=str1, inline=False)
        embed.add_field(name="🔄 혹시,", value="롤계정 닉네임이 변경되셨나요? 저에게 새로운 커맨드를 입력해주세요! \n(**/업데이트**)", inline=False)
        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
        return embed

    def init_embed(self):  
        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0x8e7cc3)
        embed.add_field(name="씨큐디코와 롤 계정 연동을 위해 커맨드를 입력해주세요!", value=" (/연동 롤닉네임)", inline=False)
        embed.add_field(name="예)/연동 CQ Dolphin", value="커맨드내 실수를 하셨다면, 재인증 커맨드를 입력해주세요! (/재인증)", inline=False)
        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")    
        return embed

    def change_time_to_string(self, timestruct):
        str = time.strftime("%Y년 %m월 %d일 %H시 %M분", timestruct)
        return str

    async def rank_role_give(self, member, guild, tier_name2):
        x = member

            # if tier_name1 == "CHALLENGER":
            #     role = guild.get_role(871939976974184539)
            #     await x.remove_roles(role)
            # elif tier_name1 == "GRANDMASTER":
            #     role = guild.get_role(871940017587650601)
            #     await x.remove_roles(role)
            # elif tier_name1 == "MASTER":
            #     role = guild.get_role(871940150668718080)
            #     await x.remove_roles(role)
            # elif tier_name1 == "DIAMOND":
            #     role = guild.get_role(871939946448031754)
            #     await x.remove_roles(role)
            # elif tier_name1 == "PLATINUM":
            #     role = guild.get_role(871939922049769503)
            #     await x.remove_roles(role)
            # elif tier_name1 ==  "GOLD" :
            #     role = guild.get_role(871939856723492896)
            #     await x.remove_roles(role)
            # elif tier_name1 =="SILVER" :
            #     role = guild.get_role(871939844094427216)
            #     await x.remove_roles(role)
            # elif tier_name1 =="BRONZE"  :
            #     role = guild.get_role(871933094540754945)
            #     await x.remove_roles(role)
            # elif tier_name1 =="IRON"  :
            #     role = guild.get_role(871939741241729054)
            #     await x.remove_roles(role)
            # else:
            #     print("user is unranked")

        if tier_name2 == "CHALLENGER":
            role = guild.get_role(871939976974184539)
            await x.add_roles(role)
        elif tier_name2 == "GRANDMASTER":
            role = guild.get_role(871940017587650601)
            await x.add_roles(role)    
        elif tier_name2 == "MASTER":
            role = guild.get_role(871940150668718080)
            await x.add_roles(role)    
        elif tier_name2 == "DIAMOND":
            role = guild.get_role(871939946448031754)
            await x.add_roles(role)    
        elif tier_name2 == "PLATINUM":
            role = guild.get_role(871939922049769503)
            await x.add_roles(role)    
        elif tier_name2 ==  "GOLD" :
            role = guild.get_role(871939856723492896)
            await x.add_roles(role)    
        elif tier_name2 =="SILVER" :
            role = guild.get_role(871939844094427216)
            await x.add_roles(role)     
        elif tier_name2 =="BRONZE"  :
            role = guild.get_role(871933094540754945)
            await x.add_roles(role)   
        elif tier_name2 =="IRON"  :
            role = guild.get_role(871939741241729054)
            await x.add_roles(role)   
        else:
            print("user is unranked")


    @commands.Cog.listener()
    async def on_message(self, message):    
        if message.author == self.bot.user:
            return
        
        if message.author.bot:
            return


        #obtain the context to work with
        ctx = await self.bot.get_context(message)
        user_id = message.author.id
        guild = self.bot.get_guild(427635768844877824)
        member = await guild.fetch_member(user_id)
        dm = member.dm_channel

        

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
                    
            str1 = member.name + " says: " + message.content
            print(str1)   

            if message.content == "/인증":
                embed = self.init_embed()
                await dm.send(embed=embed)

            # yet to be implemented
            elif message.content == "/업데이트":
                try:
                    stmt = "select * from league_acc_authentication where discord_id = {}".format(user_id)
                    db.execute(stmt)
                    result = db.fetchall()

                    print(result)
                    user_summoner_id = result[0][1]
                    current_summoner_name = result[0][0]
                    current_summoner_rank = result[0][3]
                    summoner = watcher.summoner.by_id('NA1', user_summoner_id)
                    print(summoner)

                    new_name = summoner["name"]
                    summoner_obj = watcher.league.by_summoner('NA1', user_summoner_id)
                    print(summoner_obj)

                    new_rank = "UNRANKED"
                    for x in summoner_obj:
                        if x["queueType"] == "RANKED_SOLO_5x5":
                            new_rank = x["tier"]

                    if current_summoner_name != new_name or current_summoner_rank != new_rank:
                        stmt2 = "update league_acc_authentication set summoner_name = '{}', summoner_rank = '{}' where discord_id = {}".format(new_name, new_rank, user_id)
                        db.execute(stmt2)
                        cnx.commit()
                        print("change successfully reflected")
                        # embed here
                        tier_name1 = current_summoner_rank
                        tier_name2 = new_rank
                        guild = self.bot.get_guild(427635768844877824)
                        x = guild.get_member(user_id)
                        
                        new_name2 = new_name + " 🌟"
                        await x.edit(nick = new_name2)

                        if tier_name1 == "CHALLENGER":
                            role = guild.get_role(871939976974184539)
                            await x.remove_roles(role)
                        elif tier_name1 == "GRANDMASTER":
                            role = guild.get_role(871940017587650601)
                            await x.remove_roles(role)
                        elif tier_name1 == "MASTER":
                            role = guild.get_role(871940150668718080)
                            await x.remove_roles(role)
                        elif tier_name1 == "DIAMOND":
                            role = guild.get_role(871939946448031754)
                            await x.remove_roles(role)
                        elif tier_name1 == "PLATINUM":
                            role = guild.get_role(871939922049769503)
                            await x.remove_roles(role)
                        elif tier_name1 ==  "GOLD" :
                            role = guild.get_role(871939856723492896)
                            await x.remove_roles(role)
                        elif tier_name1 =="SILVER" :
                            role = guild.get_role(871939844094427216)
                            await x.remove_roles(role)
                        elif tier_name1 =="BRONZE"  :
                            role = guild.get_role(871933094540754945)
                            await x.remove_roles(role)
                        elif tier_name1 =="IRON"  :
                            role = guild.get_role(871939741241729054)
                            await x.remove_roles(role)
                        else:
                            print("user is unranked")


                        if tier_name2 == "CHALLENGER":
                            role = guild.get_role(871939976974184539)
                            await x.add_roles(role)
                        elif tier_name2 == "GRANDMASTER":
                            role = guild.get_role(871940017587650601)
                            await x.add_roles(role)    
                        elif tier_name2 == "MASTER":
                            role = guild.get_role(871940150668718080)
                            await x.add_roles(role)    
                        elif tier_name2 == "DIAMOND":
                            role = guild.get_role(871939946448031754)
                            await x.add_roles(role)    
                        elif tier_name2 == "PLATINUM":
                            role = guild.get_role(871939922049769503)
                            await x.add_roles(role)    
                        elif tier_name2 ==  "GOLD" :
                            role = guild.get_role(871939856723492896)
                            await x.add_roles(role)    
                        elif tier_name2 =="SILVER" :
                            role = guild.get_role(871939844094427216)
                            await x.add_roles(role)     
                        elif tier_name2 =="BRONZE"  :
                            role = guild.get_role(871933094540754945)
                            await x.add_roles(role)   
                        elif tier_name2 =="IRON"  :
                            role = guild.get_role(871939741241729054)
                            await x.add_roles(role)   
                        else:
                            print("user is unranked")

                    else:
                        print("{} tried to but there is no change to be made")
                        # embed here

                except Exception as e:
                    print(e)
            
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
                        con_chan = guild.get_channel(872539969397334057)
                        overwrite = discord.PermissionOverwrite()
                        overwrite.view_channel = False
                        await con_chan.set_permissions(member, overwrite =overwrite)
                    
                    self.rank_role_give(member, guild, summoner_tier)

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
                stmt = "select summoner_id, authenticated, summoner_name, summoner_rank from league_acc_authentication where discord_id = {} ".format(message.author.id)
                db.execute(stmt)
                result = db.fetchall()

                summoner_id = result[0][0]
                
                # This user has already been authenticated
                if result[0][1] == 1:
                    user_id = message.author.id
                    guild = self.bot.get_guild(427635768844877824)
                    member = await guild.fetch_member(user_id)
                    new_name = result[0][2] + " 🌟"
                    await member.edit(nick = new_name)

                    member_role = guild.get_role(683841495417225301)
                    roles = member.roles
                    if member_role not in roles:
                        await member.add_roles(member_role, reason ="League Account connected")
                        log_chat = guild.get_channel(870718238173044767)
                        str1 = "Added role **{}** to {} successfully. League name: **{}**".format(member_role.name, member.mention, result[0][2])
                        con_chan = guild.get_channel(872539969397334057)
                        overwrite = discord.PermissionOverwrite()
                        overwrite.view_channel = False
                        await con_chan.set_permissions(member, overwrite =overwrite)
                        await log_chat.send(str1)
                        embed = self.success_embed(result[0][2])
                        await dm.send(embed=embed)

                    self.rank_role_give(member, guild, result[0][3])

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

                        stmt2 = "select summoner_rank from league_acc_authentication where discord_id = {}".format(message.author.id)
                        db.execute(stmt2)
                        tier = db.fetchall()
                        
                        embed = self.init_success_embed(summoner_name)
                        await dm.send(embed=embed)
                        
                        # 서버 닉네임 change to summoner name + the icon, assign the rank role as well
                        user_id = message.author.id
                        guild = self.bot.get_guild(427635768844877824)
                        member = await guild.fetch_member(user_id)
                        new_name = summoner_name + " 🌟"
                        await member.edit(nick = new_name)

                        member_role = guild.get_role(683841495417225301)
                        roles = member.roles
                        if member_role not in roles:
                            log_chat = guild.get_channel(870718238173044767)
                            str1 = "Added role **{}** to {} successfully. League name: **{}**".format(member_role.name, member.mention, result[0][2])
                            await member.add_roles(member_role, reason ="League Account connected")
                            con_chan = guild.get_channel(872539969397334057)
                            overwrite = discord.PermissionOverwrite()
                            overwrite.view_channel = False
                            await con_chan.set_permissions(member, overwrite =overwrite)
                            await log_chat.send(str1)
                        
                        await self.rank_role_give(member, guild, tier[0][0])
                        
                    # authentication failed
                    else:
                        embed=discord.Embed(title="🔗 씨큐디코 롤 계정 인증/연동", description="      　", color=0xff5c5c)
                        embed.add_field(name="⛔ 계정 인증실패", value="변경된 소환사 아이콘이 확인되지 않았습니다. \n다시 연동을 실행하시려면 커맨드를 입력해주세요! **(/연동 롤닉네임)**", inline=False)
                        embed.set_footer(text="버그 혹은 건의사항은 Dolphin#0001 에게 보내주세요...")
                        await ctx.send(embed=embed)

            #3일에 한번씩
            elif message.content == "/재인증":
                three_days = 259200
                current_epoch = time.time()
                
                check = "select reauthenticate_time from league_acc_authentication where discord_id = {}".format(message.author.id)
                db.execute(check)
                result = db.fetchall()
                print(result)

                # If there is some time saved, we need to check first
                if len(result) != 0:
                    last_epoch = result[0][0]
                    if last_epoch != None:
                        if last_epoch + three_days > current_epoch:
                            # not able to reauthenticate yet... send embed here
                            # need to change last_epoch and last_epoch + three days into string
                            return

                stmt = "delete from league_acc_authentication where discord_id = {}".format(message.author.id)
                db.execute(stmt)
                cnx.commit()

                stmt2 = "delete from icon_authentication where discord_id = {}".format(message.author.id)
                db.execute(stmt2)
                cnx.commit()

                change = "update league_acc_authentication set reauthenticate_time = {} where discord_id = {}".format(current_epoch, message.author.id)
                db.execute(change)
                cnx.commit()


                # need embed here
                await ctx.send('``리셋 완료, 저에게 다시`` **/인증** ``이라고 보내주세요! (리셋 된 이상, 정회원과 랭크 권한이 사라지니 꼭 다시 계정연동을 해 주세요.)``')
                
                role_mem = guild.get_role(683841495417225301)
                list = [871939741241729054, 871933094540754945, 871939844094427216, 871939856723492896, 871940150668718080, 871940017587650601, 871939922049769503, 871939976974184539, 871939946448031754]
                for x in member.roles:
                    if x in list:
                        role_tier = guild.get_role(x)
                        await member.remove_roles(role_tier)

                await member.remove_roles(role_mem)
                
                await member.edit(nick = None)
                # save the epoch into the table!

            else:
                await ctx.send('``앗, 오타가 있어요. 저에게 /인증, /연동 닉네임, /재인증, /업데이트 중 하나를 보내주세요...``')
      
        
def setup(bot: commands.Bot):
    bot.add_cog(LeagueAccountAuthentication(bot))