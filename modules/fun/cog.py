from nextcord.ext import commands
from nextcord import File
import aiohttp
from io import BytesIO
from random import random, choice

from functions import staticValues as sv


class Fun(commands.Cog):
  """Fun features"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.command_variables = []
    self.feature_variables = []

  def checkCoffee(self, message) -> bool:
    """Check if the Feature is allowed to be used by this user and in this channel"""
    features = self.bot.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == self.qualified_name), None)
    if feature == None:
      print(f"ERROR: {self.qualified_name} feature not found")
      return False
    if not feature.isEnabled(message.guild.id):
      return False
    command = next((x for x in feature.commands if x.name == "coffee"), None)
    if command == None:
      print("ERROR: coffee command not found")
      return False
    if not command.isAllowedByMember(message.guild.id, message.author):
      return False
    if not command.isAllowedInChannel(message.guild.id, message.channel.id):
      return False
    return True

  @commands.Cog.listener('on_message')
  async def serve_coffee(self, message):
    """Serve coffee in specific channels"""
    if message.author == self.bot.user:
      return
    if not self.checkCoffee(message):
      return
    embeds = message.embeds # return list of embeds
    eContent = ''
    for embed in embeds:
      emDict = embed.to_dict()
      try:
        eContent += emDict['description']
      except:
        pass
      for e in embed.fields:
        eContent += e.name + e.value
    #Coffee reply picture
    if "coffee" in message.content.lower() or "coffee" in eContent.lower():
      url = "https://coffee.alexflipnote.dev/random"
      async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
          if resp.status != 200:
              print('Could not download file...')
          data = BytesIO(await resp.read())
          await message.channel.send(file=File(data, 'coffee_image.png'))

  def checkRandomReply(self, message) -> bool:
    """Check if the Feature is allowed to be used by this user and in this channel"""
    features = self.bot.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == self.qualified_name), None)
    if feature == None:
      print(f"ERROR: {self.qualified_name} feature not found")
      return False
    if not feature.isEnabled(message.guild.id):
      return False
    command = next((x for x in feature.commands if x.name == "randomReply"), None)
    if command == None:
      print("ERROR: randomReply command not found")
      return False
    if not command.isAllowedByMember(message.guild.id, message.author):
      return False
    if not command.isAllowedInChannel(message.guild.id, message.channel.id):
      return False
    return True
  
  @commands.Cog.listener('on_message')
  async def random_reply(self, message):
    """Random replies in specific channels"""
    if message.author == self.bot.user:
      return
    if not self.checkRandomReply(message):
      return
    #get command
    features = self.bot.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == self.qualified_name), None)
    command = next((x for x in feature.commands if x.name == "randomReply"), None)
    res = None
    if any(x in message.content.lower() for x in command.keywords[message.guild.id]):
      if random() > 0.5:
        res = choice(command.replies[message.guild.id])
    if res != None:
      await message.channel.send(res)
    return



def setup(bot: commands.Bot):
  bot.add_cog(Fun(bot))