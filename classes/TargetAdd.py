from nextcord import SelectOption, Interaction
from nextcord.ui import Select, View

from classes.Target import Target
from classes.Structure import Structure
from classes.Member import MemberClass

from functions import targetFunctions as tf


class SelectSector(Select):
  """Dropdown for sector"""
  def __init__(self,sectors:[str]):
    super().__init__(placeholder = "Select the sector",row=0,min_values=1, max_values=1)
    options = []
    for s in sectors:
      options.append(SelectOption(label=s))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.sector = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectTyp(Select):
  """Dropdown for type"""
  def __init__(self,typs:[str]):
    super().__init__(placeholder = "Select the type",row=0,min_values=1, max_values=1)
    options = []
    for t in typs:
      options.append(SelectOption(label=t))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.typ = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectLvl(Select):
  """Dropdown for lvl"""
  def __init__(self,lvls:[str]):
    super().__init__(placeholder = "Select the lvl",row=0,min_values=1, max_values=1)
    options = []
    for l in lvls:
      options.append(SelectOption(label=l))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.lvl = int(self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectCoordinates(Select):
  """Dropdown for coordinates"""
  def __init__(self,coordinates:[str]):
    super().__init__(placeholder = "Select the coordinates",row=0,min_values=1, max_values=1)
    options = []
    for c in coordinates:
      cords = f"X: {c[0]}, Y: {c[1]}"
      options.append(SelectOption(label=cords,value=f"{c[0]},{c[1]}"))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    cords = self.values[0].split(",")
    self.view.target.x = int(cords[0])
    self.view.target.y = int(cords[1])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectHour(Select):
  """Dropdown for hour"""
  def __init__(self):
    super().__init__(placeholder = "Select the hour",row=0,min_values=1, max_values=1)
    options = []
    for s in range(24):
      options.append(SelectOption(label=str(s)))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.hour = int(self.values[0])
    self.view.setHour = True
    if self.view.setMinute:
      self.view.whatNext()
      await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectMinute(Select):
  """Dropdown for minute"""
  def __init__(self):
    super().__init__(placeholder = "Select the minute",row=1,min_values=1, max_values=1)
    options = []
    for s in range(12):
      options.append(SelectOption(label=str(s*5)))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.target.minute = int(self.values[0])
    self.view.setMinute = True
    if self.view.setHour:
      self.view.whatNext()
      await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectFlag(Select):
  """Dropdown for flag"""
  def __init__(self, flags:[MemberClass]):
    super().__init__(placeholder = "Select the flag",row=1,min_values=1, max_values=1)
    options = []
    i = 0
    for f in flags:
      options.append(SelectOption(label=f.name,value=i))
      i += 1
    options.append(SelectOption(label="None"))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    if self.values[0] == "None":
      self.view.target.flag = None
    else:
      self.view.target.flag = self.view.flags[int(self.values[0])]
    tf.addTargetToDB(self.view.target,self.view.flags)
    self.view.target.name = self.view.target.typ + " lvl " + str(self.view.target.lvl)
    self.view.targets.append(self.view.target)
    content = f"You created a target:\n{self.view.target.nameStr()}"
    await interaction.response.edit_message(content=content, view = None)


class TargetAddView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,structures:[Structure], flags: [MemberClass], targets:[Target]):
    super().__init__()
    self.structures = structures
    self.target = Target()
    self.targets = targets
    self.flags = flags
    self.filteredStructures = [s for s in self.structures]
    self.setHour = False
    self.setMinute = False
    self.content = "."
    self.whatNext()
  

  def whatNext(self):
    """Function that selects the next Dropdown to present"""
    self.clear_items()
    if self.target.sector == None:
      #Get List of sectors if only one item continue to typ
      sectors = []
      for s in self.filteredStructures:
        if not(s.sector in sectors):
          sectors.append(s.sector)
      sectors = sorted(sectors)
      if len(sectors) > 1:
        self.content = "Select a Sector."
        self.add_item(SelectSector(sectors))
        return
      self.target.sector = sectors[0]
      
    if self.target.typ == None:
      #Get List of typs if only one item continue to lvl
      self.filteredStructures = [s for s in self.filteredStructures if s.sector == self.target.sector]
      typs = []
      for s in self.filteredStructures:
        if not(s.typ in typs):
          typs.append(s.typ)
      typs = sorted(typs)
      if len(typs) > 1:
        self.content = f"You selected **{self.target.sector}**.\nNow select a type:"
        self.add_item(SelectTyp(typs))
        return
      self.target.typ = typs[0]
      
    if self.target.lvl == None:
      #Get List of lvls if only one item continue to coordinates
      self.filteredStructures = [s for s in self.filteredStructures if s.typ == self.target.typ]
      lvls = []
      for s in self.filteredStructures:
        if not(s.lvl in lvls):
          lvls.append(s.lvl)
      lvls = sorted(lvls)
      if len(lvls) > 1:
        self.content = f"You selected **{self.target.typ}** in **{self.target.sector}**.\nNow select a lvl:"
        self.add_item(SelectLvl(lvls))
        return
      self.target.lvl = lvls[0]
      
    if self.target.x == None:
      #Get List of coordinates if only one item continue to hour
      testList = []
      for s in self.filteredStructures:
        if s.lvl == self.target.lvl:
          testList.append(s)
      self.filteredStructures = [s for s in self.filteredStructures if s.lvl == self.target.lvl]
      coordinates = []
      for s in self.filteredStructures:
        if not([s.x,s.y] in coordinates):
          coordinates.append([s.x,s.y])
      coordinates = sorted(coordinates)
      if len(coordinates) > 1:
        self.content = f"You selected **{self.target.typ}** lvl **{self.target.lvl}** in **{self.target.sector}**.\nNow select the coordinates:"
        self.add_item(SelectCoordinates(coordinates))
        return
      self.target.x = coordinates[0][0]
      self.target.y = coordinates[0][1]


    if self.target.hour == None:
      #Let user pick a time
      self.content = f"You selected **{self.target.typ}** lvl **{self.target.lvl}** in **{self.target.sector}** at **X: {self.target.x}, Y: {self.target.y}**.\nNow select the Time of the attack:"
      self.add_item(SelectHour())
      self.add_item(SelectMinute())
      return

    elif self.target.flag == None:
      #Let user pick a flag
      self.content = f"You selected **{self.target.typ}** lvl **{self.target.lvl}** in **{self.target.sector}** at **X: {self.target.x}, Y: {self.target.y}**.\n**@{self.target.hour:02d}:{self.target.minute:02d}**\nNow select a flag:"
      self.add_item(SelectFlag(self.flags))
      return