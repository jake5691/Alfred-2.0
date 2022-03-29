from nextcord.ui import Select, View, Button
from nextcord import SelectOption, Interaction, ButtonStyle
################
class BackButton(Button):
  """Button to navigate back"""
  def __init__(self):
    super().__init__(style=ButtonStyle.secondary, emoji="🔙", row=1)
      
  async def callback(self, interaction:Interaction):
    self.view.textChannelGroup = 0
    removeChannels = []
    for ch in self.view.children:
      if ch.row <=1:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)

    self.view.add_item(AllowedChannelsButton())
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
################
class AllowedChannelsRightButton(Button):
  """Button to navigate between selecting allowed channels"""
  def __init__(self, current, max):
    super().__init__(style=ButtonStyle.secondary, emoji="➡️", row=1)
    if current == max-1:
      self.disabled = True
    else:
      self.disabled = False
      
  async def callback(self, interaction:Interaction):
    self.view.textChannelGroup += 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row <=1:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.textChannelGroup]))
    self.view.add_item(BackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.textChannelGroup))
    self.view.add_item(AllowedChannelsRightButton(self.view.textChannelGroup, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class AllowedChannelsLeftButton(Button):
  """Button to navigate between selecting allowed channels"""
  def __init__(self, current):
    super().__init__(style=ButtonStyle.secondary, emoji="⬅️", row=1)
    if current == 0:
      self.disabled = True
    else:
      self.disabled = False
    
  async def callback(self, interaction:Interaction):
    self.view.textChannelGroup -= 1
    removeChannels = []
    for ch in self.view.children:
      if ch.row <=1:
        removeChannels.append(ch)
    for ch in removeChannels:
      self.view.remove_item(ch)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.textChannelGroup]))
    self.view.add_item(BackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.textChannelGroup))
    self.view.add_item(AllowedChannelsRightButton(self.view.textChannelGroup, len(self.view.textChannels)))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class AllowedChannelsButton(Button):
  """Button to select allowed channels"""
  def __init__(self):
    super().__init__(label="channels", style=ButtonStyle.secondary, emoji="🟢", row=0)
    
  async def callback(self, interaction:Interaction):
    toRemove = []
    for children in self.view.children:
      if children.row == 0:
        toRemove.append(children)
    for c in toRemove:
      self.view.remove_item(c)
    self.view.add_item(BackButton())
    self.view.add_item(AllowedChannelsLeftButton(self.view.textChannelGroup))
    self.view.add_item(AllowedChannelsRightButton(self.view.textChannelGroup, len(self.view.textChannels)))
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.textChannelGroup]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################
class AllowedChannels(Select):
  """Dropdown for Allowed Channels"""
  def __init__(self, allowedChannels, availableChannels):
    super().__init__(placeholder = "Select the channels you want the feature to work in.", row=0, min_values=0, max_values=len(availableChannels))

    options = []
    for c in availableChannels:
      selected = False
      if c.id in allowedChannels:
        selected = True
      options.append(SelectOption(label=c.name, value=c.id, default=selected))
    self.options = options

  async def callback(self, interaction:Interaction):
    for op in self.options:
      if str(op.value) in self.values:
        if op.value not in self.view.command.allowedChannels[self.view.guildID]:
          self.view.command.allowedChannels[self.view.guildID].append(op.value)
      else:
        if op.value in self.view.command.allowedChannels[self.view.guildID]:
          self.view.command.allowedChannels[self.view.guildID].remove(op.value)
    self.view.remove_item(self)
    self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[self.view.textChannelGroup]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class ActivateButton(Button):
  """Button to (De)Activate a feature"""
  def __init__(self, feature, guildID):
    super().__init__(style=ButtonStyle.secondary,row=0)
    if feature.enabled[guildID]:
      self.label = "deactivate"
    else:
      self.label = "activate"

  async def callback(self, interaction:Interaction):
    self.view.feature.enabled[self.view.guildID] = not(self.view.feature.enabled[self.view.guildID])
    if self.view.feature.enabled[self.view.guildID]:
      self.label = "deactivate"
    else:
      self.label = "activate"
    self.view.clear_items()
    self.view.add_item(self)
    self.view.add_item(SelectCommand(self.view.feature, self.view.command))
    self.view.add_item(SelectFeature(self.view.settings, self.view.guildID, self.view.feature))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)

################
class SelectCommand(Select):
  """Dropdown for Command"""
  def __init__(self, feature, command):
    super().__init__(placeholder = "Select the command you want to view",row=3,min_values=1, max_values=1)
    
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
    self.view.clear_items()
    self.view.add_item(SelectCommand(self.view.feature, self.view.command))
    self.view.add_item(SelectFeature(self.view.settings, self.view.guildID, self.view.feature))
    if not self.view.guildID in self.view.command.allowedChannels:
      #Create empty List if no list exists (default for allowed everywhere)
      self.view.command.allowedChannels[self.view.guildID] = []
    self.view.add_item(AllowedChannelsButton())
      #self.view.add_item(AllowedChannels(self.view.command.allowedChannels[self.view.guildID], self.view.textChannels[:24]))
    await interaction.response.edit_message(content=self.view.content(), view = self.view)
    
################    
class SelectFeature(Select):
  """Dropdown for Feature"""
  def __init__(self, settings, guildID, feature):
    super().__init__(placeholder = "Select the feature you want to view",row=4,min_values=1, max_values=1)
    
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
    self.guildID = guild.id
    self.textChannels = [guild.text_channels[x:x+25] for x in range(0, len(guild.text_channels), 25)]
    self.textChannelGroup = 0
    self.roles = [guild.roles[x:x+25] for x in range(0, len(guild.roles), 25)]
    self.roleGroup = 0
    self.text = ""
    self.content()
    self.add_item(SelectFeature(self.settings, self.guildID, self.feature))

  def content(self):
    if not self.feature:
      return "**Settings**"
      
    res = f"**{self.feature.name}**"
    if self.feature.enabled[self.guildID]:
      res += " 🟢`ACTIVE`"
    else:
      res += " 🔴`DEACTIVE`"
    res += f"\n*{self.feature.description}*\n"

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

    res += f"\n**Allowed Channels:**"
    if not self.guildID in self.command.allowedChannels:
      #Create empty List if no list exists (default for allowed everywhere)
      self.command.allowedChannels[self.guildID] = []
    if self.command.allowedChannels[self.guildID]:
      for c in self.command.allowedChannels[self.guildID]:
        res += f" <#{c}>"
    else:
      res += " `All channels (except the excluded once)`"
      
    res += f"\n**Allowed Roles:** "
    if not self.guildID in self.command.allowedRoles:
      #Create empty List if no list exists (default for allowed everywhere)
      self.command.allowedRoles[self.guildID] = []
    if self.command.allowedRoles[self.guildID]:
      for r in self.command.allowedRoles[self.guildID]:
        res += f" <#{r}>"
    else:
      res += " `All Roles (except the excluded once)`"

    res += f"\n**Excluded Channels:** "
    if not self.guildID in self.command.excludedChannels:
      #Create empty List if no list exists
      self.command.excludedChannels[self.guildID] = []
    if self.command.excludedChannels[self.guildID]:
      for c in self.command.excludedChannels[self.guildID]:
        res += f" <#{c}>"
    else:
      res += " `None`"

    res += f"\n**Excluded Roles:** "
    if not self.guildID in self.command.excludedRoles:
      #Create empty List if no list exists
      self.command.excludedRoles[self.guildID] = []
    if self.command.excludedRoles[self.guildID]:
      for r in self.command.excludedRoles[self.guildID]:
        res += f" <@!{r}>"
    else:
      res += " `None`"
    
    return res

    