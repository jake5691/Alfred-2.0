import jsons
from nextcord import User

class Feature():
  """Class to store features and their commands, also their availability per guild"""
  def __init__(self, name=str, description=str, dbKey=str):
    self.name:str = name
    self.description:str = description
    self.enabled:{int:bool} = {}
    self.commands:[Command] = []
    self.dbKey:str = dbKey
    self.variables:[(str,str)] = []

  def isEnabled(self, guild) -> bool:
    """Checks if the Feature is enabled for this guild"""
    if guild in self.enabled:
      return self.enabled[guild]
    return False

  def convertAfterLoad(self):
    """Convert loaded data from Database to correct format"""
    #enabled
    newenabled = {}
    for g in self.enabled:
      newenabled[int(g)] = self.enabled[g]
    self.enabled = newenabled
    #variables
    for variable, type_ in self.variables:
      v = getattr(self, variable)
      nv = {}
      for g in v:
        #convert value to correct type
        nvv = ""
        list = False
        if "[" in type_:
          nvv = []
          list = True
        if "str" in type_:
          if list:
            for i in v[g]:
              nvv.append(str(i))
          else:
            nvv = str(v[g])
        if "int" in type_:
          if list:
            for i in v[g]:
              nvv.append(int(i))
          else:
            nvv = int(v[g])
        #convert guildID to int
        nv[int(g)] = nvv
      setattr(self, variable, nv)
    #commands
    commands_ = []
    for c in self.commands:
      c = str(c).replace("\\","") #make sure that string can be converted to json (new emojis are converted so some \UNICODE format which is can't be part of a valid json string)
      command = jsons.loads(str(c).replace("'",'"'), Command)
      command.convertAfterLoad()
      commands_.append(command)
    self.commands = commands_

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
    self.variables:[(str,str)] = []

  def convertAfterLoad(self):
    """Convert loaded data from Database to correct format"""
    #allowed Roles
    aR = {}
    for g in self.allowedRoles:
      aR[int(g)] = self.allowedRoles[g]
    self.allowedRoles = aR
    #allowed Channels
    aC = {}
    for g in self.allowedChannels:
      aC[int(g)] = self.allowedChannels[g]
    self.allowedChannels = aC
    #excluded Roles
    eR = {}
    for g in self.excludedRoles:
      eR[int(g)] = self.excludedRoles[g]
    self.excludedRoles = eR
    #excluded Channels
    eC = {}
    for g in self.excludedChannels:
      eC[int(g)] = self.excludedChannels[g]
    self.excludedChannels = eC
    #variables
    for variable, type_ in self.variables:
      v = getattr(self, variable)
      nv = {}
      for g in v:
        #convert value to correct type
        nvv = ""
        list = False
        if "[" in type_:
          nvv = []
          list = True
        if "str" in type_:
          if list:
            for i in v[g]:
              nvv.append(str(i))
          else:
            nvv = str(v[g])
        if "int" in type_:
          if list:
            for i in v[g]:
              nvv.append(int(i))
          else:
            nvv = int(v[g])
        #convert guildID to int
        nv[int(g)] = nvv
      setattr(self, variable, nv)

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
    if isinstance(member, User):
      print(member.name)
      return False
    roles = [x.id for x in member.roles]
    if self.allowedRoles[guild] == [] and not any(x in roles for x in self.excludedRoles[guild]):
      #All roles are allowed and none of members roles are explicitly excluded
      return True
    if any(x in roles for x in self.allowedRoles[guild]):
      #Member has an allowed role
      return True
    return False