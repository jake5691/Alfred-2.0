from nextcord.ui import View, Button
from nextcord import ButtonStyle, Interaction

from functions import targetFunctions as tf



class DeleteButton(Button):
  """Button to delete all targets"""
  def __init__(self):
    super().__init__(label="Delete all",style=ButtonStyle.red, row=0)
  
  async def callback(self,interaction:Interaction):
    #Delete all targets
    tf.deleteAllTargets()
    self.view.dataCog.targets = []
    await interaction.response.edit_message(content="You successfully **deleted all targets** - ready to add new once for the next attacks.",view=None)

class CancelButton(Button):
  """Button to cancel the deletion process"""
  def __init__(self):
    super().__init__(label="Nevermind",style=ButtonStyle.grey, row=0)
  
  async def callback(self,interaction:Interaction):

    await interaction.response.edit_message(content="**Nothing** was deleted.",view=None)


class TargetDeleteView(View):
  """The view to hold the Buttons"""
  def __init__(self, dataCog):
    super().__init__()
    self.dataCog = dataCog
    self.add_item(CancelButton())
    self.add_item(DeleteButton())
    
