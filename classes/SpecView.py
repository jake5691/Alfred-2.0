from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View
from classes.Spec import specInfo






class SelectLanguage(Select):
  """Dropdown for sector"""
  def __init__(self,languages:[str]):
    super().__init__(placeholder = "Select the language",row=0,min_values=1, max_values=1)
    options = []
    for l in languages:
      options.append(SelectOption(label=l))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.specinfo.language = self.values[0]
    print (self.view.specinfo.language)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectBanner(Select):
  """Dropdown for type"""
  def __init__(self,banner:[str]):
    super().__init__(placeholder = "are you a banner castle",row=0,min_values=1, max_values=1)
    options = []
    for b in banner:
      options.append(SelectOption(label=b))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.specinfo.banner = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

lang_list = ('German', 'French')
banneropt = ('y', 'n')
class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,lang_list:[lang_list], banneropt:[banneropt]):
    super().__init__()
    self.specinfo = specInfo()
    self.lang_list = lang_list
    self.banneropt = banneropt
    self.content = "."
    self.whatNext()
    

  def whatNext(self):
    """Function that selects the next Dropdown to present"""
    self.clear_items()
    if self.specinfo.language == None:
      #Get List of sectors if only one item continue to typ
      languages = []
      for l in self.lang_list:
        if not(l in languages):
          languages.append(l)
      languages = sorted(languages)
      print(languages)
      print(len(languages))
      if len(languages) > 1:
        self.content = "Select a Language."
        self.add_item(SelectLanguage(lang_list))
        return
      self.specinfo.language = lang_list[0]
      
    if self.specinfo.banner == None:
      #Get List of typs if only one item continue to lvl
      ban = []
      for b in self.banneropt:
        if not(b in ban):
          ban.append(b)
      ban = sorted(ban)

      if len(ban) > 1:
        self.content = f"You selected **{self.specinfo.language}**.\nNow select a type:"
        self.add_item(SelectBanner(ban))
        return
      self.specinfo.banner = banneropt[0]