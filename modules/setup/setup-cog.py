from nextcord.ext import commands
from nextcord import Interaction, slash_command 
from nextcord.ui import View
from ..classes.Structure import Structure
from ..classes.Target import Target
from ..classes.TargetSelect import TargetSelect
from replit import db
import pandas as pd

gIDS = [895003315883085865]

class Setup(commands.Cog):
  """Setup of the bot, Data Handling """

  def __init__(self, bot: commands.Bot):
    self.bot = bot


def setup(bot: commands.Bot):
  bot.add_cog(Setup(bot))