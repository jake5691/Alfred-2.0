from nextcord import SelectOption, Interaction, File
from nextcord.ui import Select, View
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)
from functions.assignSpecFunc import specAdvice
from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.redSpecFunc import *
#from classes.Member import MemberClass


class SelectLanguage(Select):
  """Dropdown for language for translation"""
  def __init__(self,flags:[str]):
    super().__init__(placeholder = "Select the language",row=0,min_values=1, max_values=1)
    options = []
    for l in flags:
      options.append(SelectOption(label=l))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    if self.values[0] == '🇬🇧':
      self.view.specinfo.language = 'english'
    elif self.values[0]== '🇪🇸':
      self.view.specinfo.language = 'spanish'
    else: 
      self.view.specinfo.language = 'german'
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)




class SelectBanner(Select):
  """Dropdown for banner question"""
  def __init__(self,banner:[str]):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for b in banner:
      options.append(SelectOption(label=b))
    self.options = options
  async def callback(self, interaction:Interaction):
    self.view.specinfo.banner = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectLoyalty(Select):
  """Dropdown for loyalty question"""
  def __init__(self,opt:[str]):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for op in opt:
      options.append(SelectOption(label=op))
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinfo.loyalty = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectFullIW(Select):
  """Dropdown for full on iron and wood question"""
  def __init__(self,opt:[str]):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for op in opt:
      options.append(SelectOption(label=op))
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinfo.fulliw = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectFWMax(Select):
  """Dropdown for full on iron and wood question"""
  def __init__(self,opt:[str]):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for op in opt:
      options.append(SelectOption(label=op))
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinfo.fwmax = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectOutput(Select):
  """Dropdown for full on iron and wood question"""
  def __init__(self, channel):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    options.append(SelectOption(label="ok"))
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinput(self.view.channel)
    #await self.view.specinput(channel)
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    spec = self.view.specinfo.spec
    try:
      specAdvice(self.view, spec, groups_bl, groups_gr)
      print("spec advice complete even if it's wrong")
      blueFile = self.view.bluefile
      greenFile = self.view.greenfile
      redFile = self.view.redfile
      notes = self.view.specinfo.notes
      print(blueFile)
    #send advice
      await self.view.channel.send(content =notes)
      #if specInfo.language != 'en':
       # notes_trans = GoogleTranslator(source='auto', target=target_lang).translate(text=notes)
        #await self.view.channel.send(content =notes_trans) 
      await self.view.channel.send(file=File(blueFile))
      await self.view.channel.send(file=File(greenFile))
      await self.view.channel.send(file=File(redFile))
    except:
      await self.view.channel.send(content = "Oops, something went wrong")


flags =()
class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,flags:[flags], channel, blueFile, greenFile, redFile, user, member):
    super().__init__()
    
    self.specinfo = specInfo()
    self.channel = channel
    self.flags = flags
    self.bluefile = blueFile
    self.greenfile = greenFile
    self.redfile = redFile
    self.userid = user
    self.member = member
    self.specinfo.spec = self.member.currentSkillLvl
    self.content = "."
    self.whatNext()
    self.specinput(self.channel)

    
  def whatNext(self):
    """Function that selects the next Dropdown to present"""
    self.clear_items()
    if self.specinfo.language == None:
      #Get List of sectors if only one item continue to typ
      languages = []
      for l in self.flags:
        if not(l in languages):
          languages.append(l)
      languages = sorted(languages)
      if len(languages) > 1:
        self.content = "Language:"
        self.add_item(SelectLanguage(languages))
        return
       # [,,'🇰🇷','🇮🇩','🇷🇴','🇩🇪','🇳🇱','🇹🇷','🇫🇷','🇨🇳','🇷🇺'] 
      self.specinfo.language = 'english'
      
    if self.specinfo.banner == None:
      #Get List of typs if only one item continue to lvl
      
      opt = []
      for op in ('YES', 'NO'):
        opt.append(op)
      if len(opt) > 1:
        text = 'Are you a banner castle?'
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectBanner(opt))
        return
      self.specinfo.banner = opt[0]

    if self.specinfo.loyalty == None:
      opt = []
      for op in ('YES', 'NO'):
        opt.append(op)
      if len(opt) > 1:
        text = "Have you reached your target loyalty?"
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectLoyalty(opt))
        return
      self.specinfo.loyalty = opt[0]

    if self.specinfo.fulliw == None:
      opt = []
      for op in ('YES', 'NO'):
        opt.append(op)
      if len(opt) > 1:
        text = "Are you full on iron and wood tiles?"
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectFullIW(opt))
        return
      self.specinfo.fulliw = opt[0]

    if self.specinfo.fwmax == None:
      opt = []
      for op in ('YES', 'NO'):
        opt.append(op)
      if len(opt) > 1:
        text = "Are your Frontline Workshops at the maximum level?"
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectFWMax(opt))
        return
      self.specinfo.fwmax = opt[0]
      
    if self.specinfo.output == False:
      opt = []
      
      opt.append("OK")
      if len(opt) > 0:
        text = "Press OK to continue...this could take a few moments so please have a cup of coffee"
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectOutput(self.channel))
        return
      
      
     
      #self.add_item(self.specinput)

  def specinput(self, channel):
    #specinfo = specInfo()
    print("loyalty = ", self.specinfo.loyalty)
    #print(self.view.specinfo.loyalty)
    if self.specinfo.loyalty == 'NO':
    
      self.specinfo.notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      self.specinfo.list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    elif self.specinfo.fulliw == 'NO':
     
      self.specinfo.notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      self.specinfo.list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif self.specinfo.fwmax == 'NO':
      notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      self.specinfo.list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    else:
      self.specinfo.notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      self.specinfo.list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      self.specinfo.list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')

    
      #run spec advice
    

    
      
      
    