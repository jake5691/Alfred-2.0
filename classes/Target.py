from classes.Structure import Structure
from classes.Member import MemberClass
from nextcord import Embed
from datetime import datetime, time, timedelta
import jsons

class Target(Structure):
  def __init__(self,sector:str=None,typ:str=None,lvl:int=None,coordinates:str=None,hour:int=None,minute:int=None,comment:str=None,flag=None):
    super().__init__(sector=sector,typ=typ,lvl=lvl)
    #Expected input format for coordinates: "X: 0, Y: 0"
    self.x = int(coordinates.split(',')[0][3:]) if coordinates != None else None
    self.y = int(coordinates.split(',')[1][3:]) if coordinates != None else None
    self.hour = hour
    self.minute = minute
    self.flag = flag
    self.comment = comment
    self.reminded = False
  
  def nameStr(self) -> str:
    name = f"{self.typ} {self.lvl} - X:{self.x} Y:{self.y} @{self.hour:02d}:{self.minute:02d}"
    if isinstance(self.flag,MemberClass):
      name += f" ({self.flag.name})"
    else:
      name += " (no flag)"
    return name
  
  def targetStr(self) -> str:
    res = f"{self.typ} {self.lvl} - X:{self.x} Y:{self.y} @{self.hour:02d}:{self.minute:02d}"
    if isinstance(self.flag,MemberClass):
      res += f" Flag: {self.flag.name}"
    else:
      res += " no flag"
    if self.comment != None:
      res += f" - {self.comment}"
    return res
  
  def embedFieldValue(self):
    field = f"**{self.typ} {self.lvl} - X:{self.x} Y:{self.y} @{self.hour:02d}:{self.minute:02d}**"
    value = ""
    if isinstance(self.flag,MemberClass):
      flagID = self.flag.ownerID
      if flagID == 0:
        flagID = self.flag.id
      value += f"Flag: {self.flag.name} (<@{flagID}>)\n"
    else:
      value += "No Flag\n"
    if self.comment != None:
      value += f"{self.comment}"
    return field, value
  
  def tar2db(self, flags: [MemberClass]) -> str:
    if isinstance(self.flag,MemberClass):
      self.flag = self.flag.id
    res = jsons.dumps(self)
    if self.flagFromID(flags) == False:
      self.flag = None
    return res
  
  def flagFromID(self,flags: [MemberClass]) -> bool:
    for f in flags:
      if f.id == self.flag:
        self.flag = f
        return True
    return False
  
  def needsReminder(self):
    #Check if target still needs a reminder or was alread reminded
    if self.reminded:
      return (False,"No reminder")

    #Check if it is currently a building day (Tuesday=1, Thursday=3, Sunday=6)
    now = datetime.now() + timedelta(hours = -1, minutes=-55)
    if not(now.weekday() in [1,3,6]):
      return (False,"Off day")

    #Check if we are passed the target time -> remind
    targetTime = time(self.hour,self.minute)
    nowtime = now.time()
    diff = (nowtime.hour * 60 + nowtime.minute) - (targetTime.hour * 60 + targetTime.minute)
    if diff > 0: #Remind 5min prior to target attack
      self.reminded = True
      if diff < 10: #don't send the reminder if the attack is already 5min overdue...
        return (True, "Come online we are about to attack " + self.nameStr() + "\n")
    return (False, "Not time to attack yet")
      
  
  
  