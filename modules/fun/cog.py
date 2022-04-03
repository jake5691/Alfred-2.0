from nextcord.ext import commands
from nextcord import File
from functions import staticValues as sv
import aiohttp
from io import BytesIO
from random import random, choice


class Fun(commands.Cog):
  """Fun features"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  def checkCoffee(self, message) -> bool:
    """Check if the Feature is allowed to be used by this user and in this channel"""
    features = self.bot.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == self.qualified_name), None)
    if feature == None:
      print("ERROR feature")
      return False
    if not feature.isEnabled(message.guild.id):
      print("Not enabled")
      return False
    command = next((x for x in feature.commands if x.name == "coffee"), None)
    if command == None:
      print("ERROR command")
      return False
    if not command.isAllowedByMember(message.guild.id, message.author):
      print("Role not allowed")
      return False
    if not command.isAllowedInChannel(message.guild.id, message.channel.id):
      print("Channel not allowed")
      return False
      
    return True

  @commands.Cog.listener('on_message')
  async def serve_coffee(self, message):
    """Serve coffee in specific channels"""
    if message.author == self.bot.user:
      return
    if not self.checkCoffee(message):
      return
    coffee_channels = [sv.channel.migration_to_232, sv.channel.guests, sv.channel.eden_english, sv.channel.general, sv.channel.guild_leadership]
    if not(any(c == message.channel.id for c in coffee_channels)):
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
    
  @commands.Cog.listener('on_message')
  async def random_reply(self,message):
    """Random replies in specific channels"""
    if message.author == self.bot.user:
      return
    coffee_channels = [sv.channel.migration_to_232, sv.channel.guests, sv.channel.eden_english, sv.channel.general]
    if not(any(c == message.channel.id for c in coffee_channels)):
      return
    res = None
    if any(x in message.content.lower() for x in sv.keywords):
      if random() > 0.5:
        res = choice(sv.reply)
    if res != None:
      await message.channel.send(res)
    return



def setup(bot: commands.Bot):
  bot.add_cog(Fun(bot))