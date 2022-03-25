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


flags =['🇬🇧','🇪🇸','🇰🇷','🇮🇩','🇷🇴','🇩🇪','🇳🇱','🇹🇷','🇫🇷','🇨🇳','🇷🇺'] 

class specAdv2(commands.Cog):
  """Handle spec advice"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.flags = flags
    #self.banner = False
    #self.selectOpt = False
    #self.target_lang = 'en'
    #Load Structures

  
  
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
    

    view  = SpecView( self.flags)
    await interaction.response.send_message(content="select a language:",view=view,ephemeral = True)
    
    
    if view.specinfo.loyalty == 'NO':
    
      notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    elif view.specinfo.fulliw == 'NO':
     
      notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif view.specinfo.fwmax == 'NO':
      notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    else:
      notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')

      #run spec advice
    channel = interaction.channel
    try:
      specAdvice(specinfo.banner,list1, list2, spec, groups_bl, groups_gr)
      
    #send advice
      await channel.send(content =notes)
      if specInfo.language != 'en':
        notes_trans = GoogleTranslator(source='auto', target=target_lang).translate(text=notes)
        await channel.send(content =notes_trans) 
      await channel.send(file=File('blueSpec.png'))
      await channel.send(file=File('greenSpec.png'))
      await channel.send(file=File('redSpec.png'))
    except:
      await channel.send(content = "Oops, something went wrong")

    

def setup(bot: commands.Bot):
  bot.add_cog(specAdv2(bot))
  