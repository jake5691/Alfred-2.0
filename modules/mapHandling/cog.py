from nextcord.ext import commands
from nextcord import Interaction, SlashOption, slash_command, SelectOption 
from nextcord.ui import View, Select
from ..classes.Structure import Structure
from replit import db
import pandas as pd


gIDS = [895003315883085865]

class StructureSelect(Select):
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

  async def callback(self,interaction):
    content = "Please select the "
    print(self.values)
    if self.sector == None:
      self.sector = self.values[0]
      self.selStructures = self.structures[self.structures["sector"] == self.sector]
      self._setOptions("typ")
      self.placeholder = "Select the type"
      content += "type:"
    elif self.typ == None:
      self.typ = self.values[0]
      self.selStructures = self.structures[(self.structures["sector"] == self.sector) & (self.structures["typ"] == self.typ)]
      self._setOptions("lvl")
      self.placeholder = "Select the lvl"
      content += "lvl:"
    elif self.lvl == None:
      self.lvl = self.values[0]
      self.selStructures = self.structures[(self.structures["sector"] == self.sector) & (self.structures["typ"] == self.typ) & (self.structures["lvl"] == self.lvl)]
      self._setOptions("coordinates")
      self.placeholder = "Select the structure"
      content += "structure:"
    elif self.coordinates == None:
      self.coordinates = self.values[0]
      content = f"You selected **{self.typ}** lvl **{self.lvl}** in **{self.sector}** sector at **{self.coordinates}**"
      await interaction.response.edit_message(content=content,view=None)
      return
    await interaction.response.edit_message(content=content,view=self.view)
  
  def _setOptions(self,col:str):
    structs = self.selStructures.drop_duplicates(subset=[col])
    options = []
    for s in list(structs[col]):
      options.append(SelectOption(label=s))
    self.options = options


class Map(commands.Cog):
  """Handle Eden map data"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    try:
      allStructs = db["allStructures"]
    except:
      print("Error loading Database")
    self.allStructures = pd.DataFrame(columns=['sector','typ','lvl','coordinates'])
    for s in allStructs:
      st = Structure().db2str(s)
      self.allStructures.loc[len(self.allStructures.index)] = st.str2list()

  @slash_command(name="selectstructure",
                      description="Press send to start selecting a structure",
                      guild_ids=gIDS)
  async def selectStructures(self,
      interaction: Interaction):
    """Select specific structure by filtering via dropdown selections"""
    
    view = View()
    view.add_item(StructureSelect(self.allStructures))
    await interaction.response.send_message(content="Please select a sector:",view=view,ephemeral = True)
    

  @slash_command(name="addstructure",
                      description="Add Eden Structure to Database ( can later be set as target)",
                      guild_ids=gIDS)
  async def addStructure(self,
      interaction: Interaction,
      sector: str = SlashOption(
          name="sector",
          description="Sector that the structure is in",
          required=True),
      typ: str = SlashOption(
          name="typ",
          description="Type of the structure",
          required=True),
      lvl: int = SlashOption(
          name="lvl",
          description="Level of the structure",
          required=True),
      x: int = SlashOption(
          name="x",
          description="x-coordinate of the structure",
          required=True),
      y: int = SlashOption(
          name="y",
          description="y-coordinate of the structure",
          required=True)
    ):
    """Add Eden Structure to Database (can later be set as target)"""
    structure = Structure(sector,typ,lvl,x,y)
    try:
      allStructs = db["allStructures"]
    except:
      allStructs = []
    allStructs.append(structure.str2db())
    db["allStructures"] = allStructs

    await interaction.response.send_message(structure.printStr())

def setup(bot: commands.Bot):
  bot.add_cog(Map(bot))