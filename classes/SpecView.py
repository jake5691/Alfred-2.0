from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View
from classes.Target import Target
from classes.Structure import Structure
from classes.Member import MemberClass
from functions import targetFunctions as tf

##select language first
class SelectBanner(Select):
  """Sets whether the user is a banner castle """
  def __init__(self):
    selectOptions = [
      SelectOption(label='True', description = "is a banner castle"),
      SelectOption(label='False', description = "is not a banner castle")
    ]
    super().__init__(placeholder = "Are you a banner castle",row=0,min_values=1, max_values=1, options = selectOptions)
  
  async def callback(self, interaction:Interaction):
    #self.view.path = self.values[0]
    #self.view.whatNext()
    await interaction.response.edit_message(content="ok")


class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self):
    super().__init__()
    #self.structures = structures
    #self.target = Target()
    #self.targets = targets
    #self.flags = flags
    #self.filteredStructures = [s for s in self.structures]
    self.add_item(SelectBanner())
    
  
