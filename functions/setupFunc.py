import os
from nextcord.ext import commands
import pandas as pd
from replit import db
from classes.Stucture import Structure
from functions import staticValues as sv

def loadCogs(client: commands.Bot):
  #Load the initializing Cog
  if os.path.exists(os.path.join("modules","dataHandler","data-cog.py")):
    client.load_extension(f"modules.dataHandler.data-cog")
    print("Loaded data cog.")
  #Load all cogs
  for  folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules",folder,"cog.py")):
      client.load_extension(f"modules.{folder}.cog")

def importStructureCSV():
  ##Load eden structure information from csv and save them to Database (replaces previous entries)
  e_str = pd.read_csv(os.path.join("modules","data","eden_buildings_ALL_3.csv"),sep=";")
  db[sv.allStructures] =[]
  e = []
  for _,r in e_str.iterrows():
    st = Structure(sector=r['SECTOR'],typ=r['TYPE'],lvl=r['LVL'],x=int(r['X']),y=int(r['Y']))
    e.append(st.str2db())
  db[sv.allStructures] = e

def loadStructures() -> [Structure]:
  ##Load Strucures from Database
  allStructures = pd.DataFrame(columns=['sector','typ','lvl','coordinates'])
  try:
    allStructs = db[sv.allStructures]
  except:
    print("Error loading Database")
    return allStructures
  for s in allStructs:
    st = Structure().db2str(s)
    allStructures.loc[len(allStructures.index)] = st.str2list()
  return allStructures