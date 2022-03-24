from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View
from classes.Target import Target
from classes.Structure import Structure
from classes.Member import MemberClass
from functions import targetFunctions as tf

##select language first
class SelectLanguage(Select):
  """Sets whether the user is a banner castle """
  def __init__(self):
    selectOptions = [
      SelectOption(label='French', description = "bonjour"),
      SelectOption(label='German', description = "guten tag")
    ]
    super().__init__(placeholder = "Are you a banner castle",row=0,min_values=1, max_values=1, options = selectOptions)
  
  async def callback(self, interaction:Interaction):
    
    self.view.target_lang = self.values[0]
    print(self.view.target_lang)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)


class SelectBanner(Select):
  """Sets whether the user is a banner castle """
  def __init__(self):
    selectOptions = [
      SelectOption(label='True', description = "is a banner castle"),
      SelectOption(label='False', description = "is not a banner castle")
    ]
    super().__init__(placeholder = "Are you a banner castle",row=0,min_values=1, max_values=1, options = selectOptions)
  
  async def callback(self, interaction:Interaction):
    
    self.view.banner = self.values[0]
    print(self.view.banner)
    #self.view.whatNext()
    await interaction.response.edit_message(content=f'You selected banner is {self.banner}')


class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self):
    super().__init__()

    self.target_lang = 'NotSet'
    self.banner = 'NotSet'
    self.content = "."
    self.whatNext()

  def whatNext(self):
    #self.clear_items()
    if self.target_lang == 'NotSet':
      self.add_item(SelectLanguage())
      print(self.target_lang)
    if self.banner == 'NotSet':
      self.add_item(SelectBanner())
      print(self.banner)
    
      
      
    
  
