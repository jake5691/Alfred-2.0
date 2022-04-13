import jsons
import pandas as pd
from io import StringIO
from replit import db

from classes.Season import Season
from classes.Member import MemberClass

from functions import staticValues as sv

def loadSeasons() ->[Season]:
  #db[sv.db.seasonInfo] = []
  try:
    seasonsDB = db[sv.db.seasonInfo]
  except:
    return []
  seasons = []
  for s in seasonsDB:
    season = jsons.loads(s,Season)
    season.data = pd.read_csv(StringIO(season.data),sep=',')
    seasons.append(season)
  return seasons

def saveSeasons(seasons:[Season]):
  res = []
  for s in seasons:
    data = s.data.copy()
    s.data = s.data.to_csv()
    res.append(jsons.dumps(s))
    s.data = data
  db[sv.db.seasonInfo] = res

def closeSeason(season:Season,members: [MemberClass]) -> Season:

  for m in members:
    mData = m.loyaltyData.copy()
    mData.insert(2, "name", m.name)
    season.data = pd.concat([season.data, mData], ignore_index=True)
    m.updateLoyalty(0)
  season.closed = True
  
  return season

def getData(members:[MemberClass]):
  data = pd.DataFrame(columns=['name','loyalty','date'])

  for m in members:
    mData = m.loyaltyData.copy()
    mData.insert(2, "name", m.name)
    data = pd.concat([data, mData], ignore_index=True)
  return data