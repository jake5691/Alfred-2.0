from nextcord.ui import Select, View
from nextcord import SelectOption, Interaction

class SelectCommand(Select):
  """Dropdown for Command"""
  def __init__(self, feature):
    super().__init__(placeholder = "Select the command you want to view",row=3,min_values=1, max_values=1)
    
    options = []
    for idx, f in enumerate(feature.commands):
      options.append(SelectOption(label=f.name, description=f.description[:99], value=idx))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    
    self.view.command = self.view.feature.commands[int(self.values[0])]
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
class SelectFeature(Select):
  """Dropdown for Feature"""
  def __init__(self, settings):
    super().__init__(placeholder = "Select the feature you want to view",row=4,min_values=1, max_values=1)
    
    options = []
    for idx, f in enumerate(settings):
      options.append(SelectOption(label=f.name, description=f.description[:99], value=idx))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.command = None
    self.view.feature = self.view.settings[int(self.values[0])]
    self.view.clear_items()
    self.view.add_item(self)
    self.view.add_item(SelectCommand(self.view.feature))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

class SettingsView(View):
  """The view to hold the Settings Menu"""
  def __init__(self,settings, guildID):
    super().__init__()
    self.settings = settings
    self.feature = None
    self.command = None
    self.guild = guildID
    self.text = ""
    self.content()
    self.add_item(SelectFeature(settings))

  def content(self):
    if not self.feature:
      return "**Settings**"
      
    res = f"**{self.feature.name}**\n*{self.feature.description}*\n"

    args = ""
    if not self.command:
      for com in self.feature.commands:
        for arg in com.arguments:
          args += f" `{arg}`"
        res += f"\n**{com.name}**{args} - {com.typ}\n*{com.description}*"
      return res

    for arg in self.command.arguments:
      args += f" `{arg}`"
    res += f"**{self.command.name}**{args} - {self.command.typ}\n*{self.command.description}*\n"

    res += f"\n**Allowed Channels:** "

    res += f"\n**Allowed Roles:** "

    res += f"\n**Excluded Channels:** "

    res += f"\n**Excluded Roles:** "
    
    return res

    