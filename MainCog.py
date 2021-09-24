from dotenv import load_dotenv
import discord, os, asyncio, champlist, random, mysql.connector, voice_channel_title, logging, time
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from dpyConsole import Console


cnx = mysql.connector.connect(user=os.getenv("mysql_user"), password =os.getenv("mysql_pw") ,
                              host=os.getenv("mysql_host"), database =os.getenv("mysql_db") )
db = cnx.cursor()
cnx.autocommit = True

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        if not isinstance(ctx.channel, discord.DMChannel):
            print(message.author.display_name + " says " + message.content + " in " + message.channel.name)

        if message.author == self.bot.user:
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
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(427635768844877824)
        print(guild)
        hello = "안녕하세요 {}님,".format(member.name)
        embed=discord.Embed(title=hello, description="**씨큐**에 오신 것을 환영합니다!", color=0x8e7cc3)
        rule_channel = guild.get_channel(617210515134873611)
        general =  guild.get_channel(432756157497475092)
        print(general.name)
        rules = "・더 원활한 씨큐디코 사용을 위해, {} 을 참고해주세요!".format(rule_channel.mention)
        embed.add_field(name="**#1**", value=rules, inline=False)
        ch1 =  guild.get_channel(870709677644713994)
        ch2 =  guild.get_channel(872539969397334057)
        embed.add_field(name="**#2**", value="・준회원 권한 획득 방법 > {} \n・정회원 권한 획득 방법 > {}".format(ch1.mention, ch2.mention), inline=False)
        await general.send("{}".format(member.mention))
        await general.send(embed=embed)
        
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
        guild = self.bot.get_guild(payload.guild_id)
        user = payload.member
        message_id = payload.message_id
        member_role = guild.get_role(484970709324398604)

        # 준회원
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
        
        # 지원자
        if message_id == 885665438472761394:
            if payload.emoji.id == 700913860235886672:
                current_channel = guild.get_channel(payload.channel_id)
                new_channel = await current_channel.clone(name="지원자 전용채널")
        
                category = discord.utils.get(guild.categories, id = 885677829075918899)
                await new_channel.edit(category = category)

                role = guild.get_role(683841495417225301)
                default_role_overwrite = discord.PermissionOverwrite()
                default_role_overwrite.view_channel = False
                await new_channel.set_permissions(role, overwrite = default_role_overwrite)

                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.send_messages = True
                await new_channel.set_permissions(user, overwrite = overwrite)

                new_role = guild.get_role(754911888487481504)
                await user.add_roles(new_role)

            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(885665438472761394)
            await message.remove_reaction(payload.emoji, user)
    
def setup(bot: commands.Bot):
    bot.add_cog(MainCog(bot))