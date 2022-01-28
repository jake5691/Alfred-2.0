from .Structure import Structure

class Target(Structure):
  def __init__(self,sector:str='',typ:str='',lvl:int=0,coordinates:str="X: 0, Y: 0",hour:int=-1,minute:int=0,comment:str=None,flag=None):
    super().__init__(sector=sector,typ=typ,lvl=lvl)
    self.x = int(coordinates.split(',')[0][3:])
    self.y = int(coordinates.split(',')[1][3:])
    self.hour = hour
    self.minute = minute
    self.flag = flag
    self.comment = comment
  
  def requiredAttackers(self,averageDemolition:int):
    """Calculate the required attacks based on given average demolition"""
    return None
  