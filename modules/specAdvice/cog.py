#blue and green specifies the  Specs and positions, and then creates the groups for that colour. It also includes some additional variables specific to that spec
#assign uses the priority list and spec points and assigns these to the Spec
#draw creates the drawing 
#import nextcord
#import os
#import pandas as pd
#os.system("pip install deep_translator")
#import random
#from keep_alive import keep_alive
from deep_translator import (GoogleTranslator)
#from replit import db

#intents = nextcord.Intents.default()
#intents.members = True
#client = nextcord.Client(intents=intents)
import os
from nextcord import File, Embed
from nextcord.ext import commands
from functions.drawSpecFunc import draw
from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.assignSpecFunc import useful_assign, most_use, extra_tile, specAdvice


class specAdv(commands.Cog):
  """Fun features"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener('on_message')

  async def giveAdvice(self,message):
    msg = message.content.lower()
    user = message.author.id
    redFile = f"drawings/red{user}.png"
    blueFile = f"drawings/blue{user}.png"
    greenFile = f"drawings/green{user}.png"
    print(msg)
    if message.author == self.bot.user or message.author.bot:
        return

    if len(msg) == 0:
        return
    
    roles = message.author.roles
    #print(roles)
    #set variable defaults
    specadv = "error"
    loy = "n"
    spec = 0
    FullIW = "n"
    FW = "n"

    #only run in spec advice channel
    if message.channel.name == 'skill-point-advice':
      target_lang = 'en'
      #await message.channel.send(roles)
      roles = message.author.roles
      #assign language from roles
      for r in roles:
        if '🇩🇪' == r.name:
          target_lang = 'german'
        elif '🇪🇸' == r.name:
          target_lang = 'spanish'
        elif '🇫🇷' == r.name:
          target_lang = 'french'
        elif '🇮🇩' == r.name:
          target_lang = 'indonesian'
        elif '🇰🇷' == r.name:
          target_lang = 'korean'
        elif '🇳🇱' == r.name:
          target_lang = 'dutch'
        elif '🇷🇴' == r.name:
          target_lang = 'romanian'
        elif '🇹🇷' == r.name:
          target_lang = 'turkish'
        elif '🇹w' == r.name:
          target_lang = 'zh-CN'
      #set aliases of advice
      advice_list = ['advice', 'advise']
        # set error message
      errormessage = "Please try again or type HELP for instructions"
      errormsgtrans = GoogleTranslator(source='auto', target=target_lang).translate(text=errormessage)
      errormsg = message.channel.send(errormsgtrans)  
      if not msg.startswith("help"):
        print("place 1")
        if not msg.startswith(tuple(advice_list)):
          msg = GoogleTranslator(source='auto', target='en').translate(text=msg)
          print("place 2")
          await errormsg

      

      if "wife" in msg:
        await message.channel.send("Getting advice about your wife from a bot will only end in tears.  Your tears."
            )
        return

      

      #send help message for anything that isn't Advice
      if msg.startswith("help"):
        helpmsg = "This channel provides advice on where to use your specialisation points.\nPlease send your information starting with ADVICE followed by answers to the following questions:\n1. Have you reached your target loyalty?(Y/N)\n2. What is your specialisation level? \n3.Have you already switched to iron/wood tiles? (Y/N)\n4. Are your Frontline Workshops maxxed? (Y/N)\nYour answers should be separated by a space\nFor example: Advice N 73 N N "
        if target_lang != 'en':
          helpmsgtrans = GoogleTranslator(source='auto', target=target_lang).translate(text=helpmsg)
          helpEmbed = Embed(description=helpmsg)
          helpEmbed.add_field(name="Translation", value=helpmsgtrans, inline=False)
        else:
          helpEmbed = Embed(description=helpmsg)
        await message.channel.send(embed=helpEmbed)

      elif msg.startswith(tuple(advice_list)):
          if len(msg) > 7:
              if msg.split(' ')[1] in ["y", "n"]:
                  loy = msg.split(' ')[1]
              else:
                    #await message.channel.send(random.choice(other_resp))
                  await errormsg
                  return
          if len(msg) > 9:
            if int(msg.split(' ')[2]) <= 160:
              userSpecPoints = int(msg.split(' ')[2])
            else:
                    #await message.channel.send(random.choice(other_resp))
              await errormsg
              await message.channel.send(
                        "please check your specialisation level is a number less than 160"
                    )
              return
          if len(msg) > 11:
            if msg.split(' ')[3] in ["y", "n"]:
                FullIW = msg.split(' ')[3]
            else:
                    #await message.channel.send(random.choice(other_resp))
              await errormsg
              return
          if len(msg) > 13:
            if msg.split(' ')[4] in ["y", "n"]:
              FW = msg.split(' ')[4]
            else:
                    #await message.channel.send(random.choice(other_resp))
              await errormsg
              return

          if loy == 'n':
            notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
            list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
            list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
          elif FullIW == 'n':
            notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
            list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
            list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
          elif FW == 'n':
            notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
            list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
            list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
          else:
        
            notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n\n"
            list1 = ('TileHonour', 'FWMat', 'ExtraTile')
            list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')
          specAdvice(list1, list2,userSpecPoints, groups_bl, groups_gr, redFile, greenFile, blueFile)
          await message.channel.send(notes)
          if target_lang != 'en':
            notes_trans = GoogleTranslator(
            source='auto', target=target_lang).translate(text=notes)
            await message.channel.send(notes_trans)
        
          
  
          await message.channel.send(file=File(blueFile))
          await message.channel.send(file=File(greenFile))
          os.remove(blueFile)
          os.remove(greenFile)
      


def setup(bot: commands.Bot):
  bot.add_cog(specAdv(bot))

