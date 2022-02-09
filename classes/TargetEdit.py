from nextcord.ui import Select, View, Button
from classes.Target import Target
from classes.Member import MemberClass
from nextcord import ButtonStyle, Interaction, SelectOption
from functions import targetFunctions as tf
from operator import attrgetter


class DoneButton(Button):
  """Button to exit the editing"""
  def __init__(self):
    super().__init__(label="Exit",style=ButtonStyle.red, row=4)
  
  async def callback(self,interaction:Interaction):
    self.view.clear_items()
    await interaction.response.edit_message(content="Finished editing, type */listtargets* to see the current targets.",view=None)

class SaveButton(Button):
  """Button to save the editing"""
  def __init__(self):
    super().__init__(label="Save",style=ButtonStyle.green, row=4)

  async def callback(self,interaction:Interaction):
    #present the target list again after saving the target
    #print(self.view.selectedTarget.name)
    tf.saveTargets(self.view.dataCog.targets,self.view.flags)
    self.view.clear_items()
    self.view.add_item(SelectTarget(self.view.dataCog.targets))
    self.view.add_item(DoneButton())
    await interaction.response.edit_message(content="Select a target to change time and/or flag",view = self.view)

class DeleteButton(Button):
  """Button to delete the selected target"""
  def __init__(self):
    super().__init__(label="Delete Target",style=ButtonStyle.red, row=4)

  async def callback(self,interaction:Interaction):
    #present the target list again after deleting the target
    #print(self.view.selectedTarget.name)
    print(self.view.selectedTargetIdx)
    print(len(self.view.dataCog.targets))
    self.view.dataCog.targets.pop(self.view.selectedTargetIdx)
    print(len(self.view.dataCog.targets))
    tf.saveTargets(self.view.dataCog.targets,self.view.flags)
    self.view.selectedTarget = None
    self.view.clear_items()
    if len(self.view.dataCog.targets) == 0:
      await interaction.response.edit_message(content="Targetlist is empty.",view=None)
      return
    self.view.add_item(SelectTarget(self.view.dataCog.targets))
    self.view.add_item(DoneButton())
    await interaction.response.edit_message(content="Select a target to change time and/or flag",view = self.view)

class SelectHour(Select):
  """Dropdown to select the hour of the attack"""
  def __init__(self):
    super().__init__(placeholder="select the hour to change it",row=0,min_values=1, max_values=1)
    options = []
    for s in range(24):
      options.append(SelectOption(label=f"{s:02d}"))
    self.options = options

  async def callback(self,interaction: Interaction):
    self.view.selectedTarget.hour = int(self.values[0])

class SelectMinute(Select):
  """Dropdown to select the hour of the attack"""
  def __init__(self):
    super().__init__(placeholder="select the minute to change it",row=1,min_values=1, max_values=1)
    options = []
    for s in range(12):
      options.append(SelectOption(label=f"{s*5:02d}"))
    self.options = options

  async def callback(self,interaction: Interaction):
    self.view.selectedTarget.minute = int(self.values[0])

class SelectFlag(Select):
  """Dropdown to select the flag"""
  def __init__(self,flags:[MemberClass]):
    super().__init__(placeholder="select the flag to change it",row=2,min_values=1, max_values=1)
    self.flags = flags
    options = []
    i = 0
    for s in self.flags:
      options.append(SelectOption(label=f"{s.name}",value=i))
      i+=1
    options.append(SelectOption(label="None"))
    self.options = options

  async def callback(self,interaction: Interaction):
    if self.values[0] == "None":
      self.view.selectedTarget.flag = None
    else:
      self.view.selectedTarget.flag = self.flags[int(self.values[0])]


class SelectTarget(Select):
  """Dropdown to select a target to edit"""
  def __init__(self, targets:[Target]):
    super().__init__(placeholder="select the target to edit",row=0,min_values=1, max_values=1)
    options = []
    i =  0
    for t in targets:
      name = f"{t.name} (X: {t.x}, Y: {t.y})"
      options.append(SelectOption(label=name,value=i))
      i += 1
    self.options = options

  async def callback(self,interaction: Interaction):
    self.view.selectedTarget = self.view.dataCog.targets[int(self.values[0])]
    self.view.selectedTargetIdx = int(self.values[0])
    self.view.clear_items()
    self.view.add_item(SelectHour())
    self.view.add_item(SelectMinute())
    self.view.add_item(SelectFlag(self.view.flags))
    self.view.add_item(SaveButton())
    self.view.add_item(DeleteButton())
    self.view.add_item(DoneButton())
    await interaction.response.edit_message(content=f"**Edit:** {self.view.selectedTarget.name}\n*values you don't want to change you don't need to select*",view = self.view)
    

class TargetEditView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,dataCog):
    super().__init__()
    self.dataCog = dataCog
    self.dataCog.targets = sorted(self.dataCog.targets, key=attrgetter('hour', 'minute'))
    self.selectedTarget = None
    self.flags = self.dataCog.getFlags()
    self.add_item(SelectTarget(self.dataCog.targets))
    self.add_item(DoneButton())