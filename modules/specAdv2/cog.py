from nextcord.ext import commands
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message
from functions import staticValues as sv
from operator import attrgetter
from nextcord.utils import get
from classes.TargetAdd import TargetAddView

class specAdv2(commands.Cog):
  """Handle spec advice"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #self.banner = False
    #self.selectOpt = False
    #self.target_lang = 'en'
    #Load Structures

  
  
  @slash_command(name="specadviceadvanced",
                      description="Press send to add a target by selecting it.",
                      guild_ids=sv.gIDS)
  async def addTarget(self,
      interaction: Interaction):
    """spec advice"""
    #Check if user has Permission
    if not(sv.channel.skill_point_advice == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    

    view = TargetAddView(self.structures, self.dataCog.getFlags(),self.dataCog.targets)
    await interaction.response.send_message(content="Please select a sector:",view=view,ephemeral = True)

def setup(bot: commands.Bot):
  bot.add_cog(specAdv2(bot))