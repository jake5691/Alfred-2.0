from nextcord import SelectOption 
from nextcord.ui import Select
import pandas as pd

class TargetSelect(Select):
  def __init__(self,structures:pd.DataFrame):
    super().__init__(placeholder = "Select the sector")
    self.sector = None
    self.typ = None
    self.lvl = None
    self.coordinates = None
    self.structures = structures.copy()
    self.selStructures = structures.copy()
    self._setOptions("sector")
    self.min_values = 1
    self.max_values = 1
    self._oneOption = False
    self._finished = False

  async def callback(self,interaction):
    content = "Please select the "
    print(self.values)
    if self.sector == None:
      content = self._setSector(content)
    elif self.typ == None:
      content = self._setTyp(content)
    elif self.lvl == None:
      content = self._setLvl(content)
    elif self.coordinates == None:
      content = self._setCoordinates(content)
    
    if self._finished:
      await interaction.response.edit_message(content=content,view=None)
    else:
      await interaction.response.edit_message(content=content,view=self.view)
  
  def _setSector(self,content:str):
    self.sector = self.values[0]
    self.selStructures = self.structures[self.structures["sector"] == self.sector]
    self._oneOption = self._setOptions("typ")
    if self._oneOption:
      #Skip presenting if only one option available
      content = self._setTyp(content)
    else:
      self.placeholder = "Select the type"
      content += "type:"
    return content
  
  def _setTyp(self,content:str):
    if self._oneOption:
      self.tpy = self.options[0].label
    else:
      self.typ = self.values[0]
    self.selStructures = self.structures[(self.structures["sector"] == self.sector) & (self.structures["typ"] == self.typ)]
    self._oneOption = self._setOptions("lvl")
    if self._oneOption:
      #Skip presenting if only one option available
      content = self._setLvl(content)
    else:
      self.placeholder = "Select the lvl"
      content += "lvl:"
    return content
  
  def _setLvl(self,content:str):
    if self._oneOption:
      self.lvl = self.options[0].label
    else:
      self.lvl = self.values[0]
    self.selStructures = self.structures[(self.structures["sector"] == self.sector) & (self.structures["typ"] == self.typ) & (self.structures["lvl"] == self.lvl)]
    self._oneOption = self._setOptions("coordinates")
    if self._oneOption:
      #Skip presenting if only one option available
      content = self._setCoordinates(content)
    else:
      self.placeholder = "Select the structure"
      content += "structure:"
    return content

  def _setCoordinates(self,content:str):
    if self._oneOption:
      self.coordinates = self.options[0].label
    else:
      self.coordinates = self.values[0]
    content = f"You selected **{self.typ}** lvl **{self.lvl}** in **{self.sector}** sector at **{self.coordinates}**"
    self._finished = True
    return content

  def _setOptions(self,col:str):
    structs = self.selStructures.drop_duplicates(subset=[col])
    options = []
    for s in list(structs[col]):
      options.append(SelectOption(label=s))
    self.options = options
    if len(options) == 1:
      return True
    else:
      return False