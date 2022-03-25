from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)






class SelectLanguage(Select):
  """Dropdown for language"""
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
    #self.view.specinfo.language = self.values[0]
    print (self.view.specinfo.language)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectBanner(Select):
  """Dropdown for banner question"""
  def __init__(self,banner:[str]):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for b in banner:
      #bt = GoogleTranslator(source='auto', target=target_lang).translate(text=b)
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
      #opt = GoogleTranslator(source='auto', target=target_lang).translate(text=op)
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
      #opt = GoogleTranslator(source='auto', target=target_lang).translate(text=op)
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
      #opt = GoogleTranslator(source='auto', target=target_lang).translate(text=op)
      options.append(SelectOption(label=op))
    self.options = options

  async def callback(self, interaction:Interaction):
    self.view.specinfo.fwmax = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

flags =()
class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,flags:[flags]):
    super().__init__()
    self.specinfo = specInfo()
    #self.lang_list = lang_list
    self.flags = flags
    self.content = "."
    self.whatNext()

    
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
    