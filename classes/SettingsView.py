from nextcord.ui import Select, View, Button, Modal, TextInput
from nextcord import SelectOption, Interaction, ButtonStyle
from replit import db
import jsons

################
class CommandBackButton(Button):
  """Button to navigate back"""
  def __init__(self):
    super().__init__(style=ButtonStyle.blurple, emoji="🔙", row=4)
      
  async def callback(self, interaction:Interaction):
    self.view.group = 0
    self.view.variable = None
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    if self.view.command.variables != []:
      self.view.add_item(SelectCommandVariable(self.view.command, self.view.variable))
    self.view.add_item(ExcludedChannelsButton())
    self.view.add_item(AllowedChannelsButton())
    self.view.add_item(ExcludedRolesButton())
    self.view.add_item(AllowedRolesButton())
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class ExcludedChannelsRightButton(Button):
  """Button to navigate between selecting excluded channels"""
  def __init__(self, current, max):
    super().__init__(label="Next", style=ButtonStyle.secondary, row=4)
    if current == max-1:
      self.disabled = True
    else:
      self.disabled = False
      
  async def callback(self, interaction:Interaction):
    self.view.group += 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(ExcludedChannels(self.view.command.excludedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedChannelsLeftButton(self.view.group))
    self.view.add_item(ExcludedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view=self.view)
    
################
class ExcludedChannelsLeftButton(Button):
  """Button to navigate between selecting excluded channels"""
  def __init__(self, current):
    super().__init__(label="Prev", style=ButtonStyle.secondary, row=4)
    if current == 0:
      self.disabled = True
    else:
      self.disabled = False
    
  async def callback(self, interaction:Interaction):
    self.view.group -= 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(ExcludedChannels(self.view.command.excludedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedChannelsLeftButton(self.view.group))
    self.view.add_item(ExcludedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view=self.view)

################
class ExcludedChannelsButton(Button):
  """Button to select excluded channels"""
  def __init__(self):
    super().__init__(label="#", style=ButtonStyle.red, emoji="🔴", row=3)
    
  async def callback(self, interaction:Interaction):
    toRemove = []
    for children in self.view.children:
      if children.row >= 2:
        toRemove.append(children)
    for c in toRemove:
      self.view.remove_item(c)
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedChannelsLeftButton(self.view.group))
    self.view.add_item(ExcludedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    self.view.add_item(ExcludedChannels(self.view.command.excludedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class ExcludedChannels(Select):
  """Dropdown for Excluded Channels"""
  def __init__(self, excludedChannels, availableChannels):
    super().__init__(placeholder = "Channels the command should NOT work in.", row=3, min_values=0, max_values=len(availableChannels))

    options = []
    for c in availableChannels:
      selected = False
      if c.id in excludedChannels:
        selected = True
      options.append(SelectOption(label=c.name, value=c.id, default=selected))
    self.options = options

  async def callback(self, interaction:Interaction):
    if self.values != []:
      self.view.command.allowedChannels[self.view.guildID] = []
    for op in self.options:
      if str(op.value) in self.values:
        if op.value not in self.view.command.excludedChannels[self.view.guildID]:
          self.view.command.excludedChannels[self.view.guildID].append(op.value)
      else:
        if op.value in self.view.command.excludedChannels[self.view.guildID]:
          self.view.command.excludedChannels[self.view.guildID].remove(op.value)
    db[self.view.feature.dbKey] = jsons.dumps(self.view.feature)
    self.view.remove_item(self)
    self.view.add_item(ExcludedChannels(self.view.command.excludedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class ExcludedRolesRightButton(Button):
  """Button to navigate between selecting excluded roles"""
  def __init__(self, current, max):
    super().__init__(label="Next", style=ButtonStyle.secondary, row=4)
    if current == max-1:
      self.disabled = True
    else:
      self.disabled = False
      
  async def callback(self, interaction:Interaction):
    self.view.group += 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(ExcludedRolesSelect(self.view.command.excludedRoles[self.view.guildID], self.view.roles[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedRolesLeftButton(self.view.group))
    self.view.add_item(ExcludedRolesRightButton(self.view.group, len(self.view.roles)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class ExcludedRolesLeftButton(Button):
  """Button to navigate between selecting excluded roles"""
  def __init__(self, current):
    super().__init__(label="Prev", style=ButtonStyle.secondary, row=4)
    if current == 0:
      self.disabled = True
    else:
      self.disabled = False
    
  async def callback(self, interaction:Interaction):
    self.view.group -= 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(ExcludedRolesSelect(self.view.command.excludedRoles[self.view.guildID], self.view.roles[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedRolesLeftButton(self.view.group))
    self.view.add_item(ExcludedRolesRightButton(self.view.group, len(self.view.roles)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class ExcludedRolesButton(Button):
  """Button to select excluded roles"""
  def __init__(self):
    super().__init__(label="@", style=ButtonStyle.red, emoji="🔴", row=3)
    
  async def callback(self, interaction:Interaction):
    toRemove = []
    for children in self.view.children:
      if children.row >= 2:
        toRemove.append(children)
    for c in toRemove:
      self.view.remove_item(c)
    self.view.add_item(CommandBackButton())
    self.view.add_item(ExcludedRolesLeftButton(self.view.group))
    self.view.add_item(ExcludedRolesRightButton(self.view.group, len(self.view.roles)))
    self.view.add_item(ExcludedRolesSelect(self.view.command.excludedRoles[self.view.guildID], self.view.roles[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class ExcludedRolesSelect(Select):
  """Dropdown for excluded Roles"""
  def __init__(self, excludedRoles, availableRoles):
    super().__init__(placeholder = "Roles that should NOT be able to use the command.", row=3, min_values=0, max_values=len(availableRoles))

    options = []
    for r in availableRoles:
      selected = False
      if r.id in excludedRoles:
        selected = True
      options.append(SelectOption(label=r.name, value=r.id, default=selected))
    self.options = options

  async def callback(self, interaction:Interaction):
    if self.values != []:
      self.view.command.allowedRoles[self.view.guildID] = []
    for op in self.options:
      if str(op.value) in self.values:
        if op.value not in self.view.command.excludedRoles[self.view.guildID]:
          self.view.command.excludedRoles[self.view.guildID].append(op.value)
      else:
        if op.value in self.view.command.excludedRoles[self.view.guildID]:
          self.view.command.excludedRoles[self.view.guildID].remove(op.value)
    db[self.view.feature.dbKey] = jsons.dumps(self.view.feature)
    self.view.remove_item(self)
    self.view.add_item(ExcludedRolesSelect(self.view.command.excludedRoles[self.view.guildID], self.view.roles[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class AllowedRolesRightButton(Button):
  """Button to navigate between selecting allowed roles"""
  def __init__(self, current, max):
    super().__init__(label="Next", style=ButtonStyle.secondary, row=4)
    if current == max-1:
      self.disabled = True
    else:
      self.disabled = False
      
  async def callback(self, interaction:Interaction):
    self.view.group += 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedRolesSelect(self.view.command.allowedRoles[self.view.guildID], self.view.roles[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedRolesLeftButton(self.view.group))
    self.view.add_item(AllowedRolesRightButton(self.view.group, len(self.view.roles)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class AllowedRolesLeftButton(Button):
  """Button to navigate between selecting allowed roles"""
  def __init__(self, current):
    super().__init__(label="Prev", style=ButtonStyle.secondary, row=4)
    if current == 0:
      self.disabled = True
    else:
      self.disabled = False
    
  async def callback(self, interaction:Interaction):
    self.view.group -= 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedRolesSelect(self.view.command.allowedRoles[self.view.guildID], self.view.roles[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedRolesLeftButton(self.view.group))
    self.view.add_item(AllowedRolesRightButton(self.view.group, len(self.view.roles)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class AllowedRolesButton(Button):
  """Button to select allowed roles"""
  def __init__(self):
    super().__init__(label="@", style=ButtonStyle.green, emoji="🟢", row=3)
    
  async def callback(self, interaction:Interaction):
    toRemove = []
    for children in self.view.children:
      if children.row >= 2:
        toRemove.append(children)
    for c in toRemove:
      self.view.remove_item(c)
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedRolesLeftButton(self.view.group))
    self.view.add_item(AllowedRolesRightButton(self.view.group, len(self.view.roles)))
    self.view.add_item(AllowedRolesSelect(self.view.command.allowedRoles[self.view.guildID], self.view.roles[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class AllowedRolesSelect(Select):
  """Dropdown for Allowed Roles"""
  def __init__(self, allowedRoles, availableRoles):
    super().__init__(placeholder = "Roles that should be able to use the feature.", row=3, min_values=0, max_values=len(availableRoles))

    options = []
    for r in availableRoles:
      selected = False
      if r.id in allowedRoles:
        selected = True
      options.append(SelectOption(label=r.name, value=r.id, default=selected))
    self.options = options

  async def callback(self, interaction:Interaction):
    if self.values != []:
      self.view.command.excludedRoles[self.view.guildID] = []
    for op in self.options:
      if str(op.value) in self.values:
        if op.value not in self.view.command.allowedRoles[self.view.guildID]:
          self.view.command.allowedRoles[self.view.guildID].append(op.value)
      else:
        if op.value in self.view.command.allowedRoles[self.view.guildID]:
          self.view.command.allowedRoles[self.view.guildID].remove(op.value)
    db[self.view.feature.dbKey] = jsons.dumps(self.view.feature)
    self.view.remove_item(self)
    self.view.add_item(AllowedRolesSelect(self.view.command.allowedRoles[self.view.guildID], self.view.roles[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class AllowedChannelsRightButton(Button):
  """Button to navigate between selecting allowed channels"""
  def __init__(self, current, max):
    super().__init__(style=ButtonStyle.secondary, emoji="➡️", row=4)
    if current == max-1:
      self.disabled = True
    else:
      self.disabled = False
      
  async def callback(self, interaction:Interaction):
    self.view.group += 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.group))
    self.view.add_item(AllowedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class AllowedChannelsLeftButton(Button):
  """Button to navigate between selecting allowed channels"""
  def __init__(self, current):
    super().__init__(style=ButtonStyle.secondary, emoji="⬅️", row=4)
    if current == 0:
      self.disabled = True
    else:
      self.disabled = False
    
  async def callback(self, interaction:Interaction):
    self.view.group -= 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row >=2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.group))
    self.view.add_item(AllowedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class AllowedChannelsButton(Button):
  """Button to select allowed channels"""
  def __init__(self):
    super().__init__(label="#", style=ButtonStyle.green, emoji="🟢", row=3)
    
  async def callback(self, interaction:Interaction):
    toRemove = []
    for children in self.view.children:
      if children.row >= 2:
        toRemove.append(children)
    for c in toRemove:
      self.view.remove_item(c)
    self.view.add_item(CommandBackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.group))
    self.view.add_item(AllowedChannelsRightButton(self.view.group, len(self.view.textChannels)))
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class AllowedChannels(Select):
  """Dropdown for Allowed Channels"""
  def __init__(self, allowedChannels, availableChannels):
    super().__init__(placeholder = "Channels the command should work in.", row=3, min_values=0, max_values=len(availableChannels))

    options = []
    for c in availableChannels:
      selected = False
      if c.id in allowedChannels:
        selected = True
      options.append(SelectOption(label=c.name, value=c.id, default=selected))
    self.options = options

  async def callback(self, interaction:Interaction):
    if self.values != []:
      self.view.command.excludedChannels[self.view.guildID] = []
    for op in self.options:
      if str(op.value) in self.values:
        if op.value not in self.view.command.allowedChannels[self.view.guildID]:
          self.view.command.allowedChannels[self.view.guildID].append(op.value)
      else:
        if op.value in self.view.command.allowedChannels[self.view.guildID]:
          self.view.command.allowedChannels[self.view.guildID].remove(op.value)
    db[self.view.feature.dbKey] = jsons.dumps(self.view.feature)
    self.view.remove_item(self)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.group]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class ActivateButton(Button):
  """Button to (De)Activate a feature"""
  def __init__(self, feature, guildID):
    super().__init__(row=3)
    if feature.enabled[guildID]:
      self.label = "deactivate"
      self.style = ButtonStyle.red
    else:
      self.label = "activate"
      self.style = ButtonStyle.green

  async def callback(self, interaction:Interaction):
    self.view.feature.enabled[self.view.guildID] = not(self.view.feature.enabled[self.view.guildID])
    if self.view.feature.enabled[self.view.guildID]:
      self.label = "deactivate"
      self.style = ButtonStyle.red
    else:
      self.label = "activate"
      self.style = ButtonStyle.green
    db[self.view.feature.dbKey] = jsons.dumps(self.view.feature)
    self.view.clear_items()
    self.view.add_item(self)
    self.view.add_item(SelectCommand(self.view.feature, self.view.command))
    self.view.add_item(SelectFeature(self.view.settings, self.view.guildID, self.view.feature))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class AddValueCommandVariableButton(Button):
  """Button add values to command variable"""
  def __init__(self, variable, list):
    super().__init__(label="Add", style= ButtonStyle.green, row=4)
    self.variable = variable
    self.list = list

  async def callback(self, interaction:Interaction):
    await interaction.response.send_modal(ModalCommandVariable(self.view, interaction, self.variable[0], self.list))
    
################
class RemoveValueCommandVariableSelect(Select):
  """Dropdown to remove values from the variable"""
  def __init__(self, command, var, guildID):
    super().__init__(placeholder="Select the values you want to remove", row=3, min_values=0, max_values=len(getattr(command,var[0])[guildID]))
    self.var = var
    options = []
    for val in getattr(command, self.var[0])[guildID]:
      options.append(SelectOption(label=val[:99]))
    self.options = options
    
  async def callback(self, interaction:Interaction):
    for v in self.values:
      getattr(self.view.command,self.var[0])[self.view.guildID].remove(v)
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class RemoveValueCommandVariableButton(Button):
  """Button remove values to command variable"""
  def __init__(self, command, variable, guildID):
    super().__init__(label="Remove", style= ButtonStyle.red, row=4)
    self.enabled = False
    self.var = variable
    if guildID in getattr(command,self.var[0]):
      if len(getattr(command,self.var[0])[guildID]) > 0:
        self.enabled = True

  async def callback(self, interaction:Interaction):
    removeChannels = []
    for ch in self.view.children:
      if ch.row >= 3:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(RemoveValueCommandVariableSelect(self.view.command, self.var, self.view.guildID))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
  
################
class ModalCommandVariable(Modal):
  """Modal for text input for command variables"""
  def __init__(self, view, interaction_, variable, list):
    super().__init__(title=f"Add values for {variable}")
    self.view = view
    self.interaction_ = interaction_
    count = 1
    if list:
      count = 5
    for _ in range(count):
      self.add_item(TextInput(label="add value", placeholder="add a new value", required=False))
      
  async def callback(self, interaction: Interaction):
    var = self.view.command.variables[self.view.variable]
    for c in self.children:
      if c.value == "":
        continue
      if self.view.guildID in getattr(self.view.command,var[0]):
        getattr(self.view.command,var[0])[self.view.guildID].append(c.value)
      else:
        getattr(self.view.command,var[0])[self.view.guildID] = [c.value]
    await self.interaction_.edit_original_message(content=self.view.content(), view = self.view)
    
################
class SelectCommandVariable(Select):
  """Dropdown for command Variable"""
  def __init__(self, command, variable):
    super().__init__(placeholder = "Select the variable you want to edit", row=2, min_values=1, max_values=1)
    
    options = []
    for idx, f in enumerate(command.variables):
      selected = False
      if idx == variable:
        selected = True
      op = SelectOption(label=f[0], description=f[1], value=idx, default=selected)
      options.append(op)
    self.options = options
  
  async def callback(self, interaction:Interaction):
    variable = self.view.command.variables[int(self.values[0])]
    self.view.variable = int(self.values[0])
    self.view.group = 0
    removeChannels = []
    for ch in self.view.children:
      if ch.row >= 2:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(SelectCommandVariable(self.view.command, self.view.variable))
    list = False
    if "[" in variable[1]:
      list = True
    if "str" in variable[1]:
      if list:
        #back
        self.view.add_item(CommandBackButton())
        #add
        self.view.add_item(AddValueCommandVariableButton(variable, list))
        #remove
        self.view.add_item(RemoveValueCommandVariableButton(self.view.command, variable, self.view.guildID))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class SelectCommand(Select):
  """Dropdown for Command"""
  def __init__(self, feature, command):
    super().__init__(placeholder = "Select the command you want to view",row=1,min_values=1, max_values=1)
    
    options = []
    for idx, f in enumerate(feature.commands):
      selected = False
      if command:
        if f == command:
          selected = True
      op = SelectOption(label=f.name, description=f.description[:99], value=idx, default=selected)
      options.append(op)
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.command = self.view.feature.commands[int(self.values[0])]
    self.view.variable = None
    self.view.clear_items()
    self.view.add_item(SelectCommand(self.view.feature, self.view.command))
    self.view.add_item(SelectFeature(self.view.settings, self.view.guildID, self.view.feature))
    if self.view.command.variables != []:
      self.view.add_item(SelectCommandVariable(self.view.command, self.view.variable))
    if not self.view.guildID in self.view.command.allowedChannels:
      #Create empty List if no list exists (default for allowed everywhere)
      self.view.command.allowedChannels[self.view.guildID] = []
    self.view.add_item(ExcludedChannelsButton())
    self.view.add_item(AllowedChannelsButton())
    self.view.add_item(ExcludedRolesButton())
    self.view.add_item(AllowedRolesButton())
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################    
class SelectFeature(Select):
  """Dropdown for Feature"""
  def __init__(self, settings, guildID, feature):
    super().__init__(placeholder = "Select the feature you want to view",row=0,min_values=1, max_values=1)
    
    options = []
    for idx, f in enumerate(settings):
      selected = False
      if feature:
        if feature == f:
          selected = True
      if f.enabled[guildID]:
        emoji = "🟢"
      else:
        emoji = "🔴"
      options.append(SelectOption(label=f.name, emoji=emoji, description=f.description[:99], value=idx, default=selected))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.command = None
    self.view.variable = None
    self.view.feature = self.view.settings[int(self.values[0])]
    self.view.clear_items()
    self.view.add_item(SelectFeature(self.view.settings, self.view.guildID, self.view.feature))
    self.view.add_item(SelectCommand(self.view.feature, self.view.command))
    self.view.add_item(ActivateButton(self.view.feature, self.view.guildID))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class SettingsView(View):
  """The view to hold the Settings Menu"""
  def __init__(self, settings, guild):
    super().__init__(timeout=None)
    self.settings = settings
    self.feature = None
    self.command = None
    self.variable = None
    self.guildID = guild.id
    self.textChannels = [guild.text_channels[x:x+25] for x in range(0, len(guild.text_channels), 25)]
    self.roles = [guild.roles[x:x+25] for x in range(0, len(guild.roles), 25)]
    self.group = 0
    self.text = ""
    self.content()
    self.add_item(SelectFeature(self.settings, self.guildID, self.feature))

  def content(self):
    if not self.feature:
      return "**Settings**"
    
    #feature
    res = f"**{self.feature.name}**"
    if self.feature.enabled[self.guildID]:
      res += " 🟢`ACTIVE`"
    else:
      res += " 🔴`DEACTIVE`"
    res += f"\n*{self.feature.description}*\n"
    #commands
    args = ""
    if not self.command:
      for com in self.feature.commands:
        for arg in com.arguments:
          args += f" `{arg}`"
        res += f"\n**{com.name}**{args} - {com.typ}\n*{com.description}*"
      db[self.feature.dbKey] = jsons.dumps(self.feature)
      return res
    #command
    for arg in self.command.arguments:
      args += f" `{arg}`"
    res += f"**{self.command.name}**{args} - {self.command.typ}\n*{self.command.description}*\n"

    #variables
    if self.command.variables != []:
      res += f"\n**Variables:**\n"
      for var, type_ in self.command.variables:
        res += f"**{var}**: `{type_}` = "
        if self.guildID in getattr(self.command, var):
          value = f"{getattr(self.command, var)[self.guildID]}"
          if self.variable != None:
            res += value + "\n"
            continue
          if len(value) > 30:
            value = value[:27] + "..."
          elif len(value) == 0:
            value = "-"
          res += value
        res += "\n"

      if self.variable != None:
        db[self.feature.dbKey] = jsons.dumps(self.feature)
        return res
      

    #check if guild is already in the settings list
    if self.guildID not in self.command.allowedChannels:
      self.command.allowedChannels[self.guildID] = []
    if self.guildID not in self.command.excludedChannels:
      self.command.excludedChannels[self.guildID] = []
    if self.guildID not in self.command.allowedRoles:
      self.command.allowedRoles[self.guildID] = []
    if self.guildID not in self.command.excludedRoles:
      self.command.excludedRoles[self.guildID] = []
    #Channels
    if self.command.allowedChannels[self.guildID] == [] and self.command.excludedChannels[self.guildID] == []:
      res += "\nThis command is **allowed in all channels.**\n*To exclude some channels use 🔴#, to only allow specific ones use 🟢#*"
    elif self.command.excludedChannels[self.guildID] != []:
      res += "\nThis command is **allowed in all channels except:**"
      for c in self.command.excludedChannels[self.guildID]:
        res += f" <#{c}>"
      res += "\n*To exclude some more channels use 🔴#, to only allow specific ones use 🟢# (resets exclutions)*"
    else:
      res += "\nThis command is **allowed only in those channels:**"
      for c in self.command.allowedChannels[self.guildID]:
        res += f" <#{c}>"
      res += "\n*To allow all channels but exclude some specific ones use 🔴#, to add more channels use 🟢#.*"
      
    #Roles
    if self.command.allowedRoles[self.guildID] == [] and self.command.excludedRoles[self.guildID] == []:
      res += "\n\nThis command is **allowed to be used by all roles.**\n*To exclude some roles use 🔴@, to only allow it for specific roles use 🟢@*"
    elif self.command.excludedRoles[self.guildID] != []:
      res += "\n\nThis command is **allowed to be used by all roles except:**"
      for r in self.command.excludedRoles[self.guildID]:
        res += f" <@&{r}>"
      res += "\n*To exclude some more roles use 🔴@, to only allow the use by specific ones use 🟢@ (resets exclutions)*"
    else:
      res += "\n\nThis command is **allowed only to be used only by those roles:**"
      for r in self.command.allowedRoles[self.guildID]:
        res += f" <@&{r}>"
      res += "\n*To allow all roles but exclude some specific ones use 🔴@, to add more roles use 🟢@.*"

    db[self.feature.dbKey] = jsons.dumps(self.feature)
    return res

    