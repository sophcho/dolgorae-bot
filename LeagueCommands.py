from dotenv import load_dotenv
import discord, os, asyncio, champlist
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands


load_dotenv('.env')
api_key = os.getenv("api_key")
watcher = LolWatcher(api_key)
league_version = "11.15.1"

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
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
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

    
def setup(bot: commands.Bot):
    bot.add_cog(LeagueCommands(bot))