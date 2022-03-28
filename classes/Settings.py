

class Feature():
  """Class to store features and their commands, also their availability per guild"""
  def __init__(self, name=str, description=str, dbKey=str):
    self.name:str = name
    self.description:str = description
    self.enabled:{int:bool} = {}
    self.commands:[Command] = []
    self.dbKey:str = dbKey

class Command():
  """Class to store commands and their properties, especially guild specific attributes"""
  def __init__(self, name=str, description=str, typ=str):
    self.name:str = name
    self.description:str = description
    self.typ:str = typ
    self.arguments:[str] = []
    self.allowedChannels = {}
    self.allowedRoles = {}
    self.excludedChannels = {}
    self.excludedRoles = {}