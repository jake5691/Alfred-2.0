from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View
from classes.Target import Target
from classes.Structure import Structure

from functions import targetFunctions as tf


class TopPriorities(Select):
  """Select top 3 priorities"""
  def __init__(self):
    super().__init__(placeholder = "Select the sector",row=0,min_values=3, max_values=3)
    options = ['TileHonour', 'FWMat', 'ExtraTile', 'UpgradeBuild', 'LoyaltySpeedGroup']
    #self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.prio1 = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class NextPriorities(Select):
  """Select top 3 priorities"""
  def __init__(self):
    super().__init__(placeholder = "Select the sector",row=0,min_values=1, max_values=3)
    options = ['TileHonour', 'FWMat', 'ExtraTile', 'UpgradeBuild', 'LoyaltySpeedGroup']
    #self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.prio2 = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)


class SpecAddView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self):
    super().__init__()
    self.prio1 = []
    self.prio2 = []
    self.content = "."
    self.whatNext()
  

  def whatNext(self):
    """Function that selects the next Dropdown to present"""
    self.clear_items()
    if self.prio1 == []:
      #Get List of sectors if only one item continue to ty
      
      self.content = "Select your top three priorities."
      self.add_item(TopPriorities())
      return
    
      
    if self.prio2 == []:
      self.content = "You selected **{self.prio1}**.\nPlease select two or three additional priorities:"
      self.add_item(NextPriorities())
      return
      
