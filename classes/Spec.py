# node object for spec advice

class Spec():
  def __init__(self,title:str,center:(int,int),maxLvl:int,bigCircle:bool=False):
    self.title = title
    self.maxLvl = maxLvl
    self.currentLvl = 0
    self.bigCircle = bigCircle
    self.description = "Description"
    self.center = center
    if bigCircle:
      self.size = 25
    else: 
      self.size = 15
    self.topLeft = (center[0]-self.size,center[1]-self.size)
    self.bottomRight = (center[0]+self.size,center[1]+self.size)
    self.activatable = False
    self.usefulScore = 0

class specInfo():
  def __init__(self):
    self.language = None
    self.banner = None