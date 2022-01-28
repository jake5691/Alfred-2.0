from nextcord.ext import commands
#from nextcord import Interaction, slash_command 
from classes.Structure import Structure
from functions import setupFunc as sf

gIDS = [895003315883085865]

class Data(commands.Cog):
  """Setup of the bot, Data Handling """

  def __init__(self, client: commands.Bot):
    self.client = client
    self.structures:[Structure] = sf.loadStructures()


def setup(client: commands.Bot):
  client.add_cog(Data(client))