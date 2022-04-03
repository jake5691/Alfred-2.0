

class Feature():
  """Class to store features and their commands, also their availability per guild"""
  def __init__(self, name=str, description=str, dbKey=str):
    self.name:str = name
    self.description:str = description
    self.enabled:{int:bool} = {}
    self.commands:[Command] = []
    self.dbKey:str = dbKey

  def isEnabled(self, guild) -> bool:
    """Checks if the Feature is enabled for this guild"""
    if guild in self.enabled:
      return self.enabled[guild]
    return False

class Command():
  """Class to store commands and their properties, especially guild specific attributes"""
  def __init__(self, name=str, description=str, typ=str):
    self.name:str = name
    self.description:str = description
    self.typ:str = typ
    self.arguments:[str] = []
    self.allowedChannels:{int:[int]} = {}
    self.allowedRoles:{int:[int]} = {}
    self.excludedChannels:{int:[int]} = {}
    self.excludedRoles:{int:[int]} = {}

  def isAllowedInChannel(self, guild, channel) -> bool:
    """Checks if the command is allowed in the given channel"""
    if self.allowedChannels[guild] == [] and channel not in self.excludedChannels[guild]:
      #All channels are allowed and this channel is not explicitly excluded
      return True
    if channel in self.allowedChannels[guild]:
      #This channel is explicitly allowed
      return True
    return False

  def isAllowedByMember(self, guild, member) -> bool:
    """Checks if the command is allowed to be used by this member"""
    roles = [x.id for x in member.roles]
    if self.allowedRoles[guild] == [] and not any(x in roles for x in self.excludedRoles[guild]):
      #All roles are allowed and none of members roles are explicitly excluded
      return True
    if any(x in roles for x in self.allowedRoles[guild]):
      #Member has an allowed role
      return True
    return False