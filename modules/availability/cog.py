from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption
from functions import staticValues as sv
from replit import db
from nextcord.utils import get
from operator import attrgetter
from functions import availFunc as af
from classes.availEval import AvailEvalView



class Availability(commands.Cog):
  """Availability survey handling"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @slash_command(name="startavailabilitysurvey",
                      description="Start a survey to see every players available times.",
                      guild_ids=sv.gIDS)
  async def startavailabilitysurvey(self, interaction: Interaction,
      interval: int = SlashOption(
          name="interval",
          description="What interval should each option have? e.g. 2 -> 0-2, 2-4....",
          required=True)):
    """Sending a Survey to see when Players can be online."""
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #check if command is send in correct channel
    if not(sv.channel.availability == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    #Function
    options = []
    curTime = 0
    while curTime+interval < 24:
      options.append(f"{curTime:02d}:00 - {curTime+interval:02d}:00")
      curTime += interval
    options.append(f"{curTime:02d}:00 - 24:00")
    options.append('always')
    header = "**Please react to all the times you (or your account) can be online.**\n*times refer to ingame server time*"
    survey = "```"
    reacts = sv.emojiAlph.copy()
    for o in options:
      e = reacts.pop(0)
      survey += f"\n{e} {o}"
    survey += "```"
    await interaction.response.send_message("Creating your survey now...",ephemeral=True)
    #Creating the survey
    mes = await interaction.channel.send(header+survey)
    reacts = sv.emojiAlph.copy()
    surveyDict = {}
    surveyEvalDict = {}
    for o in options:
      e = reacts.pop(0)
      surveyDict[e] = o
      surveyEvalDict[e] = []
      await mes.add_reaction(e)
    db[sv.db.availabilitySurveyMes] = mes.id
    db[sv.db.availabilitySurveyDict] = surveyDict
  
  @slash_command(name="evalavailability",
                      description="Evaluate the availability survey",
                      guild_ids=sv.gIDS)
  async def evalavailability(self, interaction: Interaction):
    """Evaluate the availability survey to see when Players can be online."""
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #check if command is send in correct channel
    if not(sv.channel.availability == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    #Function
    alwaysOption = ""
    sd = db[sv.db.availabilitySurveyDict]
    for key in sd:
      if "always" in sd[key]:
        alwaysOption = key
        break
    message = await interaction.channel.fetch_message(db[sv.db.availabilitySurveyMes])
    evalMes = "**Evaluation of the availability survey:**\n```"
    alwaysCount = 0
    optionsCount = []
    for e in message.reactions:
      if e.emoji == alwaysOption:
        alwaysCount = e.count - 1
        continue
      optionsCount.append([e.emoji, e.count-1])
    for e in optionsCount:
      evalMes += f"{e[0]} {sd[e[0]]} - {e[1]+alwaysCount}\n"
    evalMes = evalMes[:-1] + "```"
    evalMes += "\n*Give the bot a moment to load the dropdown for you so you can assign a team to the players that entered their availability.*"
    await interaction.response.send_message(evalMes, ephemeral = True)

    #check individual availabilities
    reactingMembers = []
    choicesMembers = []
    for e in message.reactions:
      mems = await e.users().flatten()
      choicesMembers.append([sd[e.emoji],mems])
      for m in mems:
        reactingMembers.append(m)
    reactingMembers = list(dict.fromkeys(reactingMembers))
    userOfInterest = sorted(reactingMembers, key=attrgetter('display_name'))
    #Filter for members without assigned team
    userOfInterest = af.removeTeamAssignees(userOfInterest, interaction.guild)
    assignRoles = [
      get(interaction.guild.roles, id=sv.roles.TeamFoxtrot),
      get(interaction.guild.roles, id=sv.roles.TeamTango),
      get(interaction.guild.roles, id=sv.roles.TeamWhiskey)
    ]
    view = AvailEvalView(userOfInterest,assignRoles,choicesMembers)

    await interaction.followup.send(content="Select a player to see their availability and assign them to a team. (only members not on a team are shown)",view=view,ephemeral = True)

    






def setup(bot: commands.Bot):
  bot.add_cog(Availability(bot))