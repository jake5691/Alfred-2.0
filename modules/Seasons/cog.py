from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption, Role, File
from operator import attrgetter
from functions import staticValues as sv
from datetime import date
from classes.Season import Season
from functions import seasonFunc as sfu

gIDS = [895003315883085865]

class Seasons(commands.Cog):
  """Create and manage Seasons"""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')
  

  @slash_command(name="createseason",
                      description="Create a RoC/Eden season for bundling loyalty Data",
                      guild_ids=gIDS)
  async def createSeason(self,interaction:Interaction,
      name:str =SlashOption(
        description="Name of the Season you want to create",
        required=True),
      typ:str =SlashOption(
        name="type",
        description="Is it a RoC, Eden: North vs. South...",
        required=True),
      startyear:int =SlashOption(
        description="Start year of the Season",
        required=True),
      startmonth:int =SlashOption(
        description="Start month of the Season",
        required=True),
      startday:int =SlashOption(
        description="Start day of the Season",
        required=True),
      endyear:int =SlashOption(
        description="End year of the Season",
        required=True),
      endmonth:int =SlashOption(
        description="End month of the Season",
        required=True),
      endday:int =SlashOption(
        description="End day of the Season",
        required=True)):
    """Create a Reign of Chaos/Eden Season"""
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #check if command is send in correct channel
    if not(sv.channel.test_channel == interaction.channel.id): #admin_moderators
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    #Function
    try:
      startdate = date(startyear,startmonth,startday)
    except ValueError:
      await interaction.response.send_message(f"please provide a valid start date.\nyou can copy your command by clicking on the blue /createseason", ephemeral = True)
      return
    try:
      enddate = date(endyear,endmonth,endday)
    except ValueError:
      await interaction.response.send_message(f"please provide a valid end date.\nyou can copy your command by clicking on the blue /createseason", ephemeral = True)
      return
    
    season = Season(name,typ,startdate,enddate)
    for s in self.dataCog.seasons:
      if (s.end < season.start) or (s.start > season.end):
        continue
      else:
        await interaction.response.send_message(f"Failed to save the season", ephemeral = True)
      return
    self.dataCog.seasons.append(season)
    sfu.saveSeasons(self.dataCog.seasons)
    
    #Send reply
    await interaction.response.send_message(f"creating a season: \n{name} - {typ}\nstart:{startdate}\nend:{enddate}", ephemeral = True)
  
  @slash_command(name="endseason",
                      description="close a season -> save all Loyalty to the database and reset all to 0",
                      guild_ids=gIDS)
  async def endSeason(self,interaction:Interaction,
      season:str=SlashOption(
        description="Select the season you want to close",
        required=True)):
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #check if command is send in correct channel
    if not(sv.channel.test_channel == interaction.channel.id): #admin_moderators
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    #Function
    season = self.dataCog.getSeasonByName(season)
    if season.closed:
      await interaction.response.send_message(f"Season **{season.name}** is already closed.", ephemeral = True)
    await interaction.response.send_message("Will close this season, wait for the response", ephemeral = True)
    season = sfu.closeSeason(season,self.dataCog.members)
    sfu.saveSeasons(self.dataCog.seasons)

    await interaction.followup.send(f"You closed Season **{season.name}**.", ephemeral = True)
  
  @endSeason.on_autocomplete("season")
  async def seasonName(self,interaction: Interaction, season: str):
    if not season:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(self.dataCog.getSeasonNames())
        return
    # send a list of nearest matches from the list of dog breeds
    get_near_name = [
        nameb for nameb in self.dataCog.getSeasonNames() if nameb.lower().startswith(season.lower())
    ]
    await interaction.response.send_autocomplete(get_near_name)
  
  @slash_command(name="seasoncsv",
                      description="Get a csv with everyones Loyalty history of the season.",
                      guild_ids=gIDS)
  async def seasoncsv(self,interaction:Interaction,
      season:str=SlashOption(
        description="Select the season you want to have a csv from",
        required=True)):
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #Function
    season = self.dataCog.getSeasonByName(season)
    await interaction.response.send_message("Wait while I prepare the data",ephemeral=True)
    f = open(f"data/{season.name}_data.csv", 'w')
    if season.closed:
      season.data.to_csv(f,index=False)
      f.close()
    else:
      sfu.getData(self.dataCog.members).to_csv(f,index=False)
      f.close
    with open(f"data/{season.name}_data.csv", 'rb') as f:
      await interaction.followup.send(f"Here is your csv file for {season.name}",ephemeral=True,file=File(f, f"{season.name}_data.csv"))
    

  @seasoncsv.on_autocomplete("season")
  async def seasonNames(self,interaction: Interaction, season: str):
    if not season:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(self.dataCog.getSeasonNames())
        return
    # send a list of nearest matches from the list of dog breeds
    get_near_name = [
        nameb for nameb in self.dataCog.getSeasonNames() if nameb.lower().startswith(season.lower())
    ]
    await interaction.response.send_autocomplete(get_near_name)


def setup(client: commands.Bot):
  client.add_cog(Seasons(client))