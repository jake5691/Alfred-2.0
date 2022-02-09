from nextcord import SelectOption, Member, Role, ButtonStyle
from nextcord.ui import Select, View, Button

class BackButton(Button):
  """Button to go back without any changes"""
  def __init__(self):
    super().__init__(label = "Back", row=1)

  async def callback(self,interaction):
    self.view.clear_items()
    self.view.add_item(AvailEvalSelect(self.view.members))
    content = "Select a player to see their availability and assign them to a team. (only members not on a team are shown)"
    await interaction.response.edit_message(content=content,view=self.view)

class AssignRole(Button):
  """Button to assign a role to the selected member"""
  def __init__(self,role: Role):
    memsInRole = 0
    for m in role.members:
      if not(m.bot):
        memsInRole +=1
    label = f"{role.name.replace('Team ','')}  ({memsInRole})"
    super().__init__(label = label, row=0,style= ButtonStyle.primary)
    self.role = role

  async def callback(self,interaction):
    print(f"Selected {self.role.name}")
    await self.view.selectedMember.add_roles(self.role)
    self.view.members.remove(self.view.selectedMember)
    self.view.clear_items()
    self.view.add_item(AvailEvalSelect(self.view.members))
    content = "Select a player to see their availability and assign them to a team. (only members not on a team are shown)"
    await interaction.response.edit_message(content=content,view=self.view)

class AvailEvalSelect(Select):
  """Dropdown menu to select a player that still needs to be assigned to a team"""
  def __init__(self, members:[Member]):
    super().__init__(placeholder = "select a player")
    self.members = members[:25]
    self._setOptions()
  
  async def callback(self,interaction):
    self.view.selectedMember = None
    for m in self.members:
      if m.id == int(self.values[0]):
        self.view.selectedMember = m
        break
    self.view.remove_item(self)
    content = f"You selected **{self.view.selectedMember.display_name}**:```"
    always = False
    for c in self.view.choices:
      if "always" in c[0]:
        if self.view.selectedMember in c[1]:
          always = True
        continue
      content += f"\n{c[0]}"
      if self.view.selectedMember in c[1]:
        content += " 🟩"
      else:
        content += " 🟥"
    content += "```"
    if always:
      content = content.replace("🟥","🟩")
    content += "\n*click on a button to assign the role*"
    for r in self.view.roles:
      self.view.add_item(AssignRole(r))
    self.view.add_item(BackButton())
    await interaction.response.edit_message(content=content,view=self.view)
  
  def _setOptions(self):
    options = []
    for m in self.members:
      options.append(SelectOption(label=m.display_name,value=m.id))
    self.options = options


class AvailEvalView(View):
  """View that holds the options to assign roles to members from the availability results"""
  def __init__(self, members:[Member], roles: [Role], choices:[]):
    super().__init__()
    self.members = members
    self.roles = roles
    self.selectedMember= None
    self.choices = choices
    self.add_item(AvailEvalSelect(members))