from nextcord.ui import Select, View, Button
from classes.Target import Target
from classes.Member import MemberClass
from nextcord import ButtonStyle, Interaction, SelectOption
from functions import targetFunctions as tf


class ExitButton(Button):
  """Button to exit the editing"""
  def __init__(self):
    super().__init__(label="Exit",style=ButtonStyle.red, row=4)
  
  async def callback(self,interaction:Interaction):
    await interaction.response.edit_message(content=f"The comment: *{self.view.comment}*\nwas not added to any target",view=None)

class SelectTarget(Select):
  """Dropdown to select a target to add the comment"""
  def __init__(self, targets:[Target]):
    super().__init__(placeholder="select the target to add the comment",row=0,min_values=1, max_values=1)
    options = []
    i =  0
    for t in targets:
      name = f"{t.name} (X: {t.x}, Y: {t.y})"
      options.append(SelectOption(label=name,value=i))
      i += 1
    self.options = options

  async def callback(self,interaction: Interaction):
    print(self.values[0])
    idx = int(self.values[0])
    self.view.targets[idx].comment = self.view.comment
    tf.saveTargets(self.view.targets, self.view.flags)
    content = "You successfully added a comment to the target:\n"
    h,v= self.view.targets[idx].embedFieldValue()
    content += f"{h}\n{v}"
    await interaction.response.edit_message(content = content, view = None)


class TargetCommentView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,targets:[Target], flags:[MemberClass], comment: str):
    super().__init__()
    self.targets = targets
    self.comment = comment
    self.flags = flags
    self.add_item(SelectTarget(targets))
    self.add_item(ExitButton())