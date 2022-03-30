from nextcord import SelectOption, Interaction, File
from nextcord.ui import Select, View
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)
from functions.assignSpecFunc import specAdvice
from functions.blueSpecFunc import groups_bl
from functions.greenSpecFunc import groups_gr

from functions.generalFunc import target_lang



class SelectLanguage(Select):
  """Dropdown for language for translation"""
  def __init__(self,flags:[str]):
    super().__init__(placeholder = "Select the language",row=0,min_values=1, max_values=1)
    options = []
    for f in flags:
      options.append(SelectOption(label=f))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.specinfo.language = target_lang(self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectAdvOpt(Select):
  """Dropdown for whether user wants to select their own or use preset values"""
  def __init__(self,pathopt):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for p, t in pathopt:
      print(p)
      options.append(SelectOption(label=p, description=t))
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.pathway = self.values[0]
    print("pathway", self.values[0])
    for i in self.values:
      print(i)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)  

class SelectPreset(Select):
  """Dropdown for preset question"""
  def __init__(self, opt):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    print(list(opt))
    for o, t in list(opt):
      print(o)
      print(t)
      options.append(SelectOption(label=o, description=t))
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.specinfo.preset = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    
class SelectBanner(Select):
  """Dropdown for banner question"""
  def __init__(self,banner):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    print(banner)
    for e, t in banner:
      options.append(SelectOption(label=e, description = t))
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
    self.view.specinput()
    #await self.view.specinput(channel)
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    spec = self.view.specinfo.spec
    try:
      await specAdvice(self.view, spec, groups_bl, groups_gr)
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
  def __init__(self,flags:[flags], channel, blueFile, greenFile, redFile,  member):
    super().__init__()
    
    self.specinfo = specInfo()
    self.channel = channel
    self.flags = flags
    self.bluefile = blueFile
    self.greenfile = greenFile
    self.redfile = redFile
    self.member = member
    self.pathway = None
    self.ready = False
    self.output = False
    self.specinfo.spec = self.member.currentSkillLvl
    self.content = "."
    self.whatNext()
    self.specinput()

    
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
      self.specinfo.language = 'english'

    if self.specinfo.banner == None:
      opt = []
      YN = ('YES', 'NO')
      for o in YN:
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=o)
        item =(o, trans)
        opt.append(item)
      text = 'Are you a banner castle?\n\n'
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'en':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectBanner(opt))
      return
      
    if self.pathway == None:
      opt = []
      for p in ('Preset', 'Select'):
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        item =(p, trans)
        opt.append(item)
      text = "Use Preset recommendations or Select your own Priorities?\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'en':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectAdvOpt(opt))
      return

    if self.pathway == "Preset" and self.ready ==False:
      trans =[]
      #preset = ('Start', 'Week1', 'Week2', 'Loyalty', 'FillIW', 'FW', 'Tile Honour')
      #p_text =('Place buildings at start of season', 'Week 1 loyalty', 'Week 2 loyalty and tilespeed', 'Increasing loyalty', 'Keep loyalty while filling on iron/wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour')
      preset = ('Loyalty', 'FillIW', 'Upgrade buildings', 'Tile Honour')
      p_text =('Increasing loyalty', 'Keep loyalty high while taking iron and wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour')
      for p in p_text:
        p_trans =  GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        trans.append(p_trans)
      opt = list(zip(preset, trans))
      text = "Select Preset option?"
      content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      self.content = content
      self.specinfo.loyalty = "na"
      self.specinfo.fwmax = "na"
      self.specinfo.fulliw = "na"
      self.ready = True
      self.add_item(SelectPreset(opt))
      return

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
      
    if self.output == False:
      opt = []
      
      opt.append("OK")
      if len(opt) > 0:
        text = "Press OK to continue...this could take a few moments so please have a cup of coffee"
        content = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        self.content = content
        self.add_item(SelectOutput(self.channel))
        return
      
      
     
      #self.add_item(self.specinput)

  def specinput(self):
    #specinfo = specInfo()
    #print("loyalty = ", self.specinfo.loyalty)
    #print(self.view.specinfo.loyalty)
  
    if self.specinfo.preset == 'Loyalty':
    
      self.specinfo.notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      self.specinfo.list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    
    elif self.specinfo.preset == 'FillIW':
     
      self.specinfo.notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      self.specinfo.list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif self.specinfo.preset == 'Upgrade buildings':
      self.specinfo.notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      self.specinfo.list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    elif self.specinfo.preset == 'Tile Honour':
      self.specinfo.notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      self.specinfo.list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      self.specinfo.list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')



      #run spec advice
    

    
      
      
    