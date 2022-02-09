from classes.Target import Target
from classes.Member import MemberClass
from functions import staticValues as sv
from replit import db
import jsons
from nextcord import Embed, Color
from math import ceil

#Add Target to db
def addTargetToDB(target:Target, flags:[MemberClass]) -> [Target]:
  targetsDB = []
  try:
    targetsDB = db[sv.db.targets]
  except:
    print("Couldn't load target list from DB.")
  targets = []
  for t in targetsDB:
    tt = jsons.loads(t,Target)
    tt.flagFromID(flags)
    targets.append(tt)
  targets.append(target)
  targetsDB.append(target.tar2db(flags))
  return targets

#Save Target List to db
def saveTargets(targets:[Target], flags:[MemberClass]) -> [Target]:
  targetsDB = []
  for t in targets:
    targetsDB.append(t.tar2db(flags))
  db[sv.db.targets] = targetsDB

#Load Targets from db
def loadTargets(flags:[MemberClass]) -> [Target]:
  dbTargets = []
  try:
    dbTargets = db[sv.db.targets]
  except:
    print("Couldn't load target list from DB.")
    return dbTargets
  targets = []
  for t in dbTargets:
    target = jsons.loads(t,Target)
    target.flagFromID(flags)
    print(target)
    targets.append(target)
  return targets

#Delete all targets from db
def deleteAllTargets():
  db[sv.db.targets] = []

#Generate Embed for calculation of attackers needed
def attackersEmbed(durability:int,avgDestruction:int) -> Embed:
  embed = Embed(
      title = "**Attack calculation**",
      description = f"Calculated with average destruction value: **{avgDestruction}**\n*you can reply to this message with a new value to update this calculation*",
      color = Color.random()
    )
  #No Banner
  totalAttacks, firstAttacks, totalAttackers,firstAttackers = _calcAttacks(durability,avgDestruction)
  noBanners = f"```Total Attacks: {totalAttacks:,}\nGuard Attacks: {firstAttacks:,}\nTotal Attackers: {totalAttackers}\nGuard Attackers: {firstAttackers}\n```"
  embed.add_field(name="**NO BANNER**",value=noBanners,inline=False)
  #Stamina Banner only
  totalAttacks, firstAttacks, totalAttackers,firstAttackers = _calcAttacks(durability,avgDestruction,pioneer=True)
  noBanners = f"```Total Attacks: {totalAttacks:,}\nGuard Attacks: {firstAttacks:,}\nTotal Attackers: {totalAttackers}\nGuard Attackers: {firstAttackers}\n```"
  embed.add_field(name="**PIONEER BANNER**",value=noBanners,inline=False)
  #Stamina and Demolition Banner 
  totalAttacks, firstAttacks, totalAttackers,firstAttackers = _calcAttacks(durability,avgDestruction,pioneer=True,raider=True)
  noBanners = f"```Total Attacks: {totalAttacks:,}\nGuard Attacks: {firstAttacks:,}\nTotal Attackers: {totalAttackers}\nGuard Attackers: {firstAttackers}\n```"
  embed.add_field(name="**PIONEER + RAIDER BANNER**",value=noBanners,inline=False)
  embed.set_footer(text=f"Durability: {durability}")
  return embed

def _calcAttacks(durability:int,avgDestruction:int,pioneer:bool=False,raider:bool=False):
  totalAttacks = ceil(durability/(avgDestruction*1.1)) if raider else ceil(durability/avgDestruction)
  firstAttacks = ceil(durability/(avgDestruction*1.1)*0.2) if raider else ceil(durability/avgDestruction*0.2)
  totalAttackers = ceil(totalAttacks/40/2) if pioneer else ceil(totalAttacks/40)
  firstAttackers = ceil(firstAttacks/40/2) if pioneer else ceil(firstAttacks/40)
  return totalAttacks, firstAttacks, totalAttackers, firstAttackers