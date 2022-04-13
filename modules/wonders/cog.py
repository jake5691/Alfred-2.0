from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command
from replit import db

from classes.WondersView import WondersView

from functions import staticValues as sv


class Wonders(commands.Cog):
  """Track the Wonders lvl of all Members"""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')

  async def checkcheck(interaction):
    featureName = "Wonders"
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

  @slash_command(name="wonders",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def updateloyskill(self, interaction: Interaction):
    """Show the Wonder Buttons to manage their lvl"""
    try:
      buttonMsg = await interaction.channel.fetch_message(db[sv.db.WONDER_BUTTON][str(interaction.guild.id)])
      await buttonMsg.delete()
    except:
      print("couldn't get old message")
    
    await interaction.send(
      content = "Press the button next to the wonder to increase it's lvl accordingly, you can also put in the lvl directly by pressing a wonder (a numberpad will be shown).",
      view = WondersView(
        dataCog=self.dataCog
      ))
    buttonMsg = await interaction.original_message()
    try:
      _ = db[sv.db.WONDER_BUTTON]
    except:
      db[sv.db.WONDER_BUTTON] = {}
    db[sv.db.WONDER_BUTTON][buttonMsg.guild.id] = buttonMsg.id
        

def setup(bot: commands.Bot):
  bot.add_cog(Wonders(bot))