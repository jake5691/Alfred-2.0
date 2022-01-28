import jsons

class Structure():

  def __init__(self,sector:str='',typ:str='',lvl:int=0,x:int=0,y:int=0):
    self.sector = sector
    self.typ = typ
    self.lvl = lvl
    self.x = x
    self.y = y
    self.points = 0
    self.durability = 0
    self.loyalty = 0
    self.damagedLoyalty = 0
  
  def printStr(self) -> str:
    res = "Sector: " + self.sector
    res += "\nType: " + self.typ + " lvl " + str(self.lvl)
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

    

