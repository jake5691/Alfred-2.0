from nextcord import SelectOption, Interaction, File
from nextcord.ui import Select, View
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)
from functions.specFunctions.assignSpecFunc import specAdvice
from functions.specFunctions.blueSpecFunc import groups_bl
from functions.specFunctions.greenSpecFunc import groups_gr
from functions.generalFunc import target_lang
import os



class SelectLanguage(Select):
  """Dropdown for language for translation"""
  def __init__(self,flags:[str]):
    super().__init__(placeholder = "Select the language",row=0,min_values=1, max_values=1)
    options = []
    for f in flags:
      options.append(SelectOption(label=f, default=False))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.specinfo.language = target_lang(self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectAdvOpt(Select):
  """Dropdown for whether user wants to select their own or use preset values"""
  def __init__(self,pathopt, content):
    super().__init__(row=0,min_values=1, max_values=1)
    options = []
    for p, t in pathopt:
      options.append(SelectOption(label=p, description=t, default=False))
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.pathway = self.values[0]
    print("pathway", self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)  

class SelectPreset(Select):
  """Dropdown to select which preset option"""
  def __init__(self, opt, content):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for o, t in list(opt):
      options.append(SelectOption(label=o, description=t, default=False))
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.specinfo.preset = self.values[0]
    self.view.clear_items()
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    
class SelectBanner(Select):
  """Dropdown for banner question"""
  def __init__(self,banner, content):
    super().__init__(row=0,min_values=1, max_values=1)
    options = []
    print(banner)
    for e, t in banner:
      options.append(SelectOption(label=e, description = t))
    self.options = options
    self.placeholder = content
  async def callback(self, interaction:Interaction):
    self.view.specinfo.banner = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectTop3(Select):
  """Dropdown for the top three priorities selection"""
  def __init__(self, opt, lookup, content):
    super().__init__(placeholder = "select three options", min_values=3, max_values=3)
    options = []
    
    for p, t in opt:  
      options.append(SelectOption(label=p, value=lookup[p], description=t, default=False)) 
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    for p in self.values:
      self.view.specinfo.list1.append(p)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectNext3(Select):
  """Dropdown for the next three priorities selection"""
  def __init__(self, opt, lookup, content, list1):
    super().__init__(placeholder = "select three options", min_values=1, max_values=3)
    options = []
    for p, t in opt:
      if lookup[p] not in list1:
        options.append(SelectOption(label=p, value=lookup[p], description=t, default=False))  
    self.placeholder = content
    self.options = options

  async def callback(self, interaction:Interaction):
    for p in self.values:
      self.view.specinfo.list2.append(p)
    self.view.specinfo.notes = "You selected your own areas of focus"
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
  

class SelectOutput(Select):
  """Dropdown to calculate and produce the drawings"""
  def __init__(self, content):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    options.append(SelectOption(label="OK", default=False))
    self.placeholder = content
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinput()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    spec = self.view.specinfo.spec
    helpText = 'Type "/specadvice" to get advice on where to use your specialisation points'
    try:
      await specAdvice(self.view, spec, groups_bl, groups_gr)
      blueFile = self.view.bluefile
      greenFile = self.view.greenfile
      redFile = self.view.redfile
      notes = self.view.specinfo.notes
    #send advice
      await self.view.channel.send(content =f"{self.view.author.mention}: {notes}")
      if self.view.specinfo.language != 'english':
        try:
          notes_trans = GoogleTranslator(source='auto', target=self.view.specinfo.language).translate(text=notes)
        except:
          notes_trans = ""
          
        await self.view.channel.send(content =f"{self.view.author.mention}: {notes_trans}") 
      await self.view.channel.send(file=File(blueFile))
      await self.view.channel.send(file=File(greenFile))
      await self.view.channel.send(file=File(redFile))
      await self.view.channel.send(content=helpText)
    except:
      await self.view.channel.send(content = f"{self.view.author.mention},Oops, something went wrong")
      await self.view.channel.send(content=helpText)

    os.remove(redFile)
    os.remove(blueFile)
    os.remove(greenFile)


class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,flags, channel, blueFile, greenFile, redFile,  member, user):
    super().__init__()
    
    self.specinfo = specInfo()
    self.author = user
    self.channel = channel
    self.flags = flags
    self.bluefile = blueFile
    self.greenfile = greenFile
    self.redfile = redFile
    self.member = member
    self.pathway = None
    self.priorityoptions = ['Loyalty', 'Extra tiles', 'One extra queue', 'Upgrade buildings', 'Tile honour', 'Income from food/marble tiles', 'Income from wood/iron tiles', 'Two extra queues', 'Three extra queues']
    self.prioritygroups = ['Loyalty', 'ExtraTile', 'OneExtQ', 'UpgradeBuild', 'TileHonour', 'CBCMat', 'FWMat', 'TwoExtQ', 'MaxQs']
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
      #get languages from those in staticvalues
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
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectBanner(opt, trans))
      return
      
    if self.pathway == None:
      opt = []
      for p in ('Preset', 'Select'):
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        item =(p, trans)
        opt.append(item)
      text = "Use Preset recommendations or Select your own Priorities?\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectAdvOpt(opt, trans))
      return

    if self.pathway == "Preset" and self.ready ==False:
      trans =[]
      #preset = ('Start', 'Week1', 'Week2', 'Loyalty', 'FillIW', 'FW', 'Tile Honour')
      #p_text =('Place buildings at start of season', 'Week 1 loyalty', 'Week 2 loyalty and tilespeed', 'Increasing loyalty', 'Keep loyalty while filling on iron/wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour')
      preset = ('Loyalty', 'Iron/Wood', 'Upgrade buildings', 'Tile Honour')
      p_text =('Increasing loyalty', 'Keep loyalty high while taking iron and wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour')
      for p in p_text:
        p_trans =  GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        trans.append(p_trans)
      opt = list(zip(preset, trans))
      text = "Select Preset option?"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.ready = True
      self.add_item(SelectPreset(opt, trans))
      return

    if self.pathway == "Select" and self.specinfo.list1 == []:
      
      opt = []

      for p in self.priorityoptions:
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        item =(p, trans)
        opt.append(item)
        #priorityOptTrans.append(trans)
      lookup = dict(zip(self.priorityoptions, self.prioritygroups))
      #text = "Sorry, this is still a work in progress.  Send jj coffee so that she can finish this more quickly.\n\n"
      text = "Please select your top three priorities.\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectTop3(opt, lookup, trans))
      return

    if self.pathway == 'Select' and self.specinfo.list2 == []:
      opt =[]
      for p in self.priorityoptions:
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        item =(p, trans)
        opt.append(item)
        #priorityOptTrans.append(trans)
      lookup = dict(zip(self.priorityoptions, self.prioritygroups))
      #text = "Sorry, this is still a work in progress.  Send jj coffee so that she can finish this more quickly.\n\n"
      text = "Please select your next priorities (minimum of 1 selection, maximum of three.\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.ready = True
      self.add_item(SelectNext3(opt, lookup, trans, self.specinfo.list1))
      return
      
      
      

    if self.output == False:
      opt = []
      opt.append("OK")
      if len(opt) > 0:
        text = "Press OK to continue...this could take a few moments so please have a cup of coffee.\n\n"
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        if self.specinfo.language != 'english':
            content = text + trans
        else:
          content = text
        self.content = content
        self.add_item(SelectOutput(GoogleTranslator(source='auto', target=self.specinfo.language).translate(text="Press ok to continue")))
        return
      


  def specinput(self):
  
    if self.specinfo.preset == 'Loyalty':
    
      self.specinfo.notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n\n"
      self.specinfo.list1 = ('Loyalty', 'CBCMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    
    elif self.specinfo.preset == 'Iron/Wood':
     
      self.specinfo.notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      self.specinfo.list1 = ('Loyalty', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif self.specinfo.preset == 'Upgrade buildings':
      self.specinfo.notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      self.specinfo.list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'Land')
    elif self.specinfo.preset == 'Tile Honour':
      self.specinfo.notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      self.specinfo.list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      self.specinfo.list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')



      #run spec advice
    

    
      
      
    