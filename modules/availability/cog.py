from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption
from replit import db
from nextcord.utils import get
from operator import attrgetter

from classes.availEval import AvailEvalView

from functions import staticValues as sv
from functions import availFunc as af




class Availability(commands.Cog):
  """Availability survey handling"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.command_variables = []
    self.feature_variables = []

  async def checkcheck(interaction):
    featureName = "Availability"
    features = interaction.client.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == featureName), None)
    #feature
    if feature == None:
      await interaction.send(f"**ERROR:** couldn't find the feature *{featureName}*, please reach out to the developers.", ephemeral=True)
      return False
    #enabled
    if not feature.isEnabled(interaction.guild.id):
      await interaction.send(f"This feature is not enabled on your server, please reach out to your Leaders for clarification.", ephemeral=True)
      return False
    #command
    command = next((x for x in feature.commands if x.name == interaction.application_command.qualified_name), None)
    if command == None:
      await interaction.send(f"**ERROR:** couldn't find the command *{interaction.application_command.qualified_name}*, please reach out to the developers.", ephemeral=True)
      return False
    #roles
    if not command.isAllowedByMember(interaction.guild.id, interaction.user):
      await interaction.send(f"You are not allowed to use this command *{command.name}*.", ephemeral=True)
      return False
    #channels
    if not command.isAllowedInChannel(interaction.guild.id, interaction.channel.id):
      await interaction.send(f"The command *{command.name}* is not allowed in this channel.", ephemeral=True)
      return False
    return True
    
  @slash_command(name="startavailabilitysurvey",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def startavailabilitysurvey(self, interaction: Interaction,
      interval: int = SlashOption(
          name="interval",
          description="What interval should each option have? e.g. 2 -> 0-2, 2-4....",
          required=True)):
    """Sending a Survey to see when Players can be online."""
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
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def evalavailability(self, interaction: Interaction):
    """Evaluate the availability survey to see when Players can be online."""
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