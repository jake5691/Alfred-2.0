from datetime import date
import pandas as pd
#from functions import seasonFunc as sf

class Season:
  def __init__(self,name: str,typ:str,start:date,end:date):
    self.name = name
    self.typ = typ
    self.start = start
    self.end = end
    self.data = pd.DataFrame(columns=['name','loyalty','date'])
    self.closed = False
  
  def save(self,seasons) -> bool:
    for s in seasons:
      if (s.end < self.start) or (s.start > self.end):
        continue
      else:
        print('there already exists a season in that time frame.')
        return False
    seasons.append(self)
    return True
    