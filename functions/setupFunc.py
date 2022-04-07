import os
import jsons
from nextcord.ext import commands
import pandas as pd
from replit import db
from operator import attrgetter

from classes.Structure import Structure
from classes.Member import MemberClass
from classes.Settings import Feature, Command
from functions import staticValues as sv

def loadCogs(client: commands.Bot):
  """Load the initializing Cog"""
  if os.path.exists(os.path.join("modules","dataHandler","data-cog.py")):
    client.load_extension(f"modules.dataHandler.data-cog")
    print("Loaded data cog.")
  #Load all cogs
  for  folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules",folder,"cog.py")):
      client.load_extension(f"modules.{folder}.cog")
      print(f"Loaded {folder} cog.")

def importStructureCSV():
  """Load eden structure information from csv and save them to Database (replaces previous entries)"""
  e_str = pd.read_csv(os.path.join("data","eden_buildings_ALL_3.csv"),sep=";")
  db[sv.db.allStructures] =[]
  e = []
  for _,r in e_str.iterrows():
    struct = Structure(sector=r['SECTOR'],
          typ=r['TYPE'],
          lvl=r['LVL'],
          x=int(r['X']),
          y=int(r['Y']),
          points=r['POINTS'],
          durability=int(r['DURABILITY']),
          loyalty=int(r['LOYALTY']),
          damagedLoyalty=int(r['DAMAGE_LOYALTY'])
          )
    e.append(struct.str2db())
  db[sv.db.allStructures] = e

def loadStructures() -> [Structure]:
  """Load Strucures from Database"""
  allStructures = pd.DataFrame(columns=['sector','typ','lvl','coordinates'])
  try:
    allStructs = db[sv.db.allStructures]
  except:
    print("Error loading Database")
    return allStructures
  everyStructures = []
  for s in allStructs:
    st = Structure().db2str(s)
    everyStructures.append(st)
    allStructures.loc[len(allStructures.index)] = st.str2list()
  return everyStructures

def loadMembers() -> [MemberClass]:
  """Load Members from Database"""
  members = []
  keys = db.prefix(sv.db.memberPrefix)
  for key in keys:
    tm = jsons.loads(db[key], MemberClass)
    tm.txt2mem()
    #if "45" in tm.name:
    #  print(tm.name)
    #  print(tm.currentSkillLvl)
    #  print(tm.skillData)
    tm = checkCurrent(tm)
    members.append(tm)
  return members

def importMemberTXT() -> [MemberClass]:
  """Load Members from txt file (export from the Bot)"""
  members = []
  f = open(os.path.join("data","members.txt"),"r")
  for m in f.readlines():
    tm = jsons.loads(m, MemberClass)
    tm.txt2mem()
    tm.save()
    members.append(tm)
  f.close()
  return members

def checkCurrent(member:MemberClass) -> MemberClass:
  if member.skillData.empty:
    member.currentSkillLvl = 0
    member.lastSkillUpdate = None
  else:
    for i in member.skillData.index:
      member.skillData.at[i,'skill'] = int(member.skillData.at[i,'skill'])
    idx = member.skillData.index[-1]
    member.currentSkillLvl = int(member.skillData.at[idx,'skill'])
    member.lastSkillUpdate = member.skillData.at[idx,'date']
  return member


def allFeatures() -> [Feature]:
  """Load all features from database"""
  res = []
  for dbKey in db.prefix("feature"):
    ff = jsons.loads(db[dbKey], Feature)
    ff.convertAfterLoad()
    res.append(ff)
  
  additionalFeatures = []
  #Fun Feature
  funFeature = Feature(name="Fun", description="Collection of fun features", dbKey="featureFun")
  #Coffee command
  coffeeCommand = Command(name="coffee", description="Send a random coffee picture to every message with the keyword **coffee** in it", typ="on_message")
  funFeature.commands.append(coffeeCommand)
  #RandomReply command
  randomReplyCommand = Command(name="randomReply", description="Send a random reply to specific keywords", typ="on_message")
  randomReplyCommand.variables = [
    ("keywords", "[str]"),
    ("replies", "[str]"),
  ]
  randomReplyCommand.keywords = {953750698552619038: ["jj"]}
  randomReplyCommand.replies = {953750698552619038: ["Hi"]}
  funFeature.commands.append(randomReplyCommand)
  additionalFeatures.append(funFeature)

  for af in additionalFeatures:
    f = next((x for x in res if x.dbKey == af.dbKey), None)
    if f == None:
      res.append(af)
      db[af.dbKey] = jsons.dumps(af)
      continue
    f.description = af.description
    f.name = af.name
    f.variables = af.variables
    for ac in af.commands:
      c = next((x for x in f.commands if x.name == ac.name), None)
      if c == None:
        f.commands.append(c)
        continue
      c.description = ac.description
      c.typ = ac.typ
      c.variables = ac.variables
      for v, t in ac.variables:
        #create attribute if it doesn't exist yet
        if v not in dir(c):
          print(f"{v} is not yet in {c.name}")
          setattr(c, v, getattr(ac, v))
          
    db[f.dbKey] = jsons.dumps(f)
  res = sorted(res, key=attrgetter('name'))
  return res

def saveFeature(f=Feature):
  db[f.dbKey] = jsons.dumps(f)
  