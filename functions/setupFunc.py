import os
from nextcord.ext import commands
import pandas as pd
from replit import db
from classes.Structure import Structure
from functions import staticValues as sv
import jsons
from classes.Member import MemberClass
from classes.Settings import Feature, Command

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
  allFeat = []
  #Coffee
  coffeeFeature = Feature(name="coffee", description="Fun feature to serve coffee", dbKey="featureCoffee")
  coffeeCommand = Command(name="coffee", description="Send a random coffee picture to every message with the keyword **coffee** in it", typ="on_message")
  coffeeFeature.commands.append(coffeeCommand)
  allFeat.append(coffeeFeature)

  #RandomReply
  randReplyFeature = Feature(name="Random Reply", description="Give random reply to keywords", dbKey="featureRandomReply")
  randomReplyCommand = Command(name="randomReply", description="Send a random reply to specific keywords", typ="on_message")
  randomReplyCommand.keywords = {}
  randomReplyCommand.replies = {}
  randReplyFeature.commands.append(randomReplyCommand)
  allFeat.append(randReplyFeature)


  ##Load stored Data
  allFeatu = []
  for f in allFeat:
    if f.dbKey not in db.keys():
      print(f.dbKey)
      print(db.prefix("feature"))
      db[f.dbKey] = jsons.dumps(f)
    ff = jsons.loads(db[f.dbKey], Feature)
    newenabled = {}
    for g in ff.enabled:
      newenabled[int(g)] = True if ff.enabled[g] == "True" else False
    ff.enabled = newenabled
    coms = []
    for c in ff.commands:
      coms.append(jsons.loads(str(c).replace("'",'"'), Command))
    ff.commands = coms
    allFeatu.append(ff)
  return allFeatu
  