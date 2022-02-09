from nextcord.ext import commands
from nextcord import File
from functions import staticValues as sv
import aiohttp
from io import BytesIO
from random import random, choice


class Fun(commands.Cog):
  """Fun features"""

  def __init__(self, client: commands.Bot):
    self.client = client

  @commands.Cog.listener('on_message')
  async def serve_coffee(self,message):
    """Serve coffee in specific channels"""
    coffee_channels = [sv.channel.migration_to_232, sv.channel.guests, sv.channel.eden_english, sv.channel.general]
    if not(any(c == message.channel.id for c in coffee_channels)):
      return
    embeds = message.embeds # return list of embeds
    eContent = ''
    for embed in embeds:
      emDict = embed.to_dict()
      eContent += emDict['description']
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



def setup(client: commands.Bot):
  client.add_cog(Fun(client))