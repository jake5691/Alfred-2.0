#blue and green specifies the  Specs and positions, and then creates the groups for that colour. It also includes some additional variables specific to that spec
#assign uses the priority list and spec points and assigns these to the Spec
#draw creates the drawing 

from deep_translator import (GoogleTranslator)
from nextcord import File, Embed
from nextcord.ext import commands
from functions.drawSpecFunc import draw
from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.assignSpecFunc import useful_assign, most_use, extra_tile, specAdvice
from functions import staticValues as sv
from replit import db
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message

class specAdv(commands.Cog):
  """Fun features"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener('on_message')
  async def giveAdvice(self,message):
    #msg = message.content.lower()
    
    if message.author.bot:
      return
      
    #only run in spec advice channel  
    if message.channel.id == sv.channel.skill_point_advice:
      
      
      #get language role if any
      target_lang = 'en'
      roles = message.author.roles
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
      if message.content.lower().startswith('help'):
        sendText = "\n\nThis channel provides advice on where to use your specialisation points.\nPlease type '/specadviceeasy' and provide input requested."
        if target_lang != 'en':
          sendTextTrans = GoogleTranslator(source='auto', target=target_lang).translate(text=sendText)  
        try:
          helpMesID = db[sv.db.specHelp]
          oldMes = await message.channel.fetch_message(helpMesID)
          await oldMes.delete()
        except:
          print("couldn't delete old help message")
        try: 
          helpMesTransId = db[sv.db.specHelpTrans]
          oldMesTrans = await message.channel.fetch_message(helpMesTransId)
          await oldMesTrans.delete()
        except:
          print("couldn't delele old translated help message")
        helpMes = await message.channel.send(content=sendText)
        db[sv.db.specHelp] = helpMes.id
        if target_lang != 'en':
          helpMesTrans = await message.channel.send(content=sendTextTrans)
          db[sv.db.specHelpTrans] = helpMesTrans.id
        await message.delete()
      #else:
        #Delete Messages that are sent in this channel after a 60s delay
        #await asyncio.sleep(60)
        #try:
         # await message.delete()
        #except:
         # print('Message could not be deleted')
  
  #get user input
  @slash_command(name="specadviceeasy",
    description="Get advice about where to place your specialisation points",
    guild_ids=sv.gIDS)
  async def specAdviceEasy(self, interaction: Interaction,
    spec:int=SlashOption(
        name="spec",
        description="How many specialisation points do you have?",
        min_value =1,
        max_value = 170,
        required=True
      ),
    banner:bool=SlashOption(
        name="banner",
        description="Are you a banner castle? (True/False)",
        required=True#,
        #default = False
      ),                       
    loy:bool=SlashOption(
        name="loy",
        description="Have you reached your target loyalty? (True/False)",
        required=True
      ),
    fwmax:bool=SlashOption(
        name="fwmax",
        description="Are your Frontline Workshops maxxed?(True/False)",
        required=True
      ),
    fulliw:bool=SlashOption(
        name="fulliw",
        description="Are you full on iron and wood tiles?(True/False)",
        required=True
      )):
    """Get spec advice based on some simple inputs"""
    print("start")
    await interaction.response.send_message("Working...this could take a minute so please have a cup of coffee while you wait.\n.\n")
    channel = interaction.channel
    if not(sv.channel.skill_point_advice == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    else:
      respOptions = f"You selected: banner:{banner}, loyalty maxxed: {loy}, Full on iron/wood tiles: {fulliw}, Frontline Workshops maxxed: {fwmax}, spec points {spec}.\n."
      await channel.send(respOptions)
    
    #Function
    target_lang = 'en'
    for r in interaction.user.roles:
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

    if loy == False:
    
      notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    elif fulliw == False:
     
      notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif fwmax == False:
      notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    else:
      notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')

      #run spec advice
    
    try:
      specAdvice(banner,list1, list2, spec, groups_bl, groups_gr)
      
    #send advice
      await channel.send(content =notes)
      if target_lang != 'en':
        notes_trans = GoogleTranslator(source='auto', target=target_lang).translate(text=notes)
        await channel.send(content =notes_trans) 
      await channel.send(file=File('blueSpec.png'))
      await channel.send(file=File('greenSpec.png'))
      await channel.send(file=File('redSpec.png'))
    except:
      await channel.send(content = "Oops, something went wrong")
    
   
      
      
      



def setup(bot: commands.Bot):
  bot.add_cog(specAdv(bot))

