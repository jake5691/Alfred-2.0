from nextcord.ext import commands

class Settings(commands.Cog):
  """Settings"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.catName = "Alfred"
    self.chanName = "Overview"

  @commands.Cog.listener('on_message')
  async def on_message(self,message):
    if message.content != "settings":
      return
    print(message.content)
      
    
  #@commands.Cog.listener('on_guild_join')
  #async def join_guild(self,guild):
  #  """Create an Alfred categorie and channel"""
  #  #check if a category and channel exist
  #  for category in guild.categories:
  #    if category.name == self.catName:
  #      for channel in category.channels:
  #        if channel.name == self.chanName:
  #          break
  #    print(f"{category.name}")
  #  pass

def setup(bot: commands.Bot):
  bot.add_cog(Settings(bot))