from nextcord.ext import commands
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message
from functions import staticValues as sv
from operator import attrgetter
from nextcord.utils import get
from classes.SpecView import SpecView
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)
from functions.drawSpecFunc import draw
from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.assignSpecFunc import useful_assign, most_use, extra_tile, specAdvice
from functions.specInput import specInput
import time

flags =['🇬🇧','🇪🇸','🇰🇷','🇮🇩','🇷🇴','🇩🇪','🇳🇱','🇹🇷','🇫🇷','🇨🇳','🇷🇺'] 


class specAdv2(commands.Cog):
  """Handle spec advice"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.flags = flags
    self.dataCog = bot.get_cog('Data')

  @slash_command(name="specadviceadvanced",
                      description="Press for spec advice.",
                      guild_ids=sv.gIDS)
  async def specadviceadvanced(self,
      interaction: Interaction):
    """spec advice"""
    #Check if user has Permission
    if not(sv.channel.skill_point_advice == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    
    channel = interaction.channel
    user = interaction.user.id
    member = self.dataCog.getMemberByID(user)    
    redFile = f"drawings/red{user}.png"
    blueFile = f"drawings/blue{user}.png"
    greenFile = f"drawings/green{user}.png"
        
    view  = SpecView( self.flags, channel, blueFile, greenFile, redFile, member)
    
    
    await interaction.response.send_message(content="select a language:",view=view,ephemeral = True)
    #waitUntil(view.specinfo.ready == True, specInput(channel, view)) #runs function  
    
    
    

def setup(bot: commands.Bot):
  bot.add_cog(specAdv2(bot))
  