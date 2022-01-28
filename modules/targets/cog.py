from nextcord.ext import commands
from nextcord import Interaction, slash_command 
from nextcord.ui import View
from ..classes.Structure import Structure
from ..classes.Target import Target
from ..classes.TargetSelect import TargetSelect
from replit import db
import pandas as pd

gIDS = [895003315883085865]

class Targets(commands.Cog):
  """Handle target data"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #Load Structures
    try:
      allStructs = db["allStructures"]
    except:
      print("Error loading Database")
    self.allStructures = pd.DataFrame(columns=['sector','typ','lvl','coordinates'])
    for s in allStructs:
      st = Structure().db2str(s)
      self.allStructures.loc[len(self.allStructures.index)] = st.str2list()

  @slash_command(name="addtarget",
                      description="Press send to add a target by selecting it.",
                      guild_ids=gIDS)
  async def addTarget(self,
      interaction: Interaction):
    """Add Target from the structure list and assign time and flag"""
    
    view = View()
    view.add_item(TargetSelect(self.allStructures))
    await interaction.response.send_message(content="Please select a sector:",view=view,ephemeral = True)
  

def setup(bot: commands.Bot):
  bot.add_cog(Targets(bot))