import jsons

class Structure():

  def __init__(self,sector:str='',typ:str='',lvl:int=0,x:int=0,y:int=0,points:int=0,durability:int=0,loyalty:int=0,damagedLoyalty:int=0):
    self.sector = sector
    self.typ = typ
    self.lvl = lvl
    self.x = x
    self.y = y
    self.points = points if lvl != None else 0
    self.durability = durability if lvl != None else 0
    self.loyalty = loyalty if lvl != None else 0
    self.damagedLoyalty = damagedLoyalty if lvl != None else 0
    if self.typ != None and self.lvl != None:
      self.name = self.typ + " lvl " + str(self.lvl)
  
  def printStr(self) -> str:
    res = "Sector: " + self.sector
    if self.typ != None and self.lvl != None:
      res += "\nType: " + self.name
    res += "\nCoordinates: X:" + str(self.x) + ", Y:" + str(self.y)
    return res
  
  def str2list(self):
    coords = "X: " + str(self.x) + ", Y: " + str(self.y)
    return [self.sector,
      str(self.typ),
      str(self.lvl),
      coords]
  
  def str2db(self) -> str:
    return jsons.dumps(self)
  
  def db2str(self,dbStr):
    self = jsons.loads(dbStr,Structure)
    return self

  def requiredAttackers(self,averageDemolition:int):
    """Calculate the required attacks based on given average demolition"""
    return None

    

