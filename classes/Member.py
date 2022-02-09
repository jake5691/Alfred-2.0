from nextcord import Member
import pandas as pd
from datetime import datetime, timedelta
import pytz
from io import StringIO
import jsons
from functions import staticValues as sv
from replit import db

class MemberClass:
  def __init__(self,m=Member,banner=False,bannerName=''):
    self.banner = banner
    self.loyaltyData = pd.DataFrame(columns=['loyalty','date'])
    self.skillData = pd.DataFrame(columns=['skill','date'])
    self.currentSkillLvl:int = 0
    self.currentLoyalty:int = 0
    self.lastSkillUpdate:datetime = None
    self.lastLoyaltyUpdate:datetime = None
    if self.banner == False:
      if m == None:
        self.name = ''
        self.id = 0
      else:
        self.name = m.display_name
        self.id = m.id
      self.ownerID = 0
      self.ownerName = ''
      self.bannerActive = False
    else:
      self.name = bannerName
      self.id = bannerName
      self.ownerID = m.id
      self.ownerName = m.display_name
      self.bannerActive = True
  
  
  def mem2txt(self) -> str:
    """Convert instance to a string"""
    #Prepping the instance so it can be converted using the "jsons.dumps"
    if self.loyaltyData.empty:
      self.loyaltyData = ""
    else:
      self.loyaltyData = self.loyaltyData.to_csv(index=False)
    if self.skillData.empty:
      self.skillData = ""
    else:
      self.skillData = self.skillData.to_csv(index=False)
    
    res = jsons.dumps(self)
    self.txt2mem()
    return res 
  
  def txt2mem(self):
    """Converting the Dataframe-csv strings to the Dataframes"""
    if self.skillData != "":
      self.skillData = pd.read_csv(StringIO(self.skillData),sep=',')
      #convert string to date
      for i in self.skillData.index:
        self.skillData.at[i,'date'] = datetime.fromisoformat(self.skillData['date'][i].split('.')[0].split('+')[0] + ".000000+00:00")
    else:
      self.skillData = pd.DataFrame(columns=['skill','date'])
    if self.loyaltyData != "":
      self.loyaltyData = pd.read_csv(StringIO(self.loyaltyData),sep=',')
      #convert string to date
      for i in self.loyaltyData.index:
        self.loyaltyData.at[i,'date'] = datetime.fromisoformat(self.loyaltyData['date'][i].split('.')[0].split('+')[0] + ".000000+00:00")
    else:
      self.loyaltyData = pd.DataFrame(columns=['loyalty','date'])
    #Convert the current date to datetime
    if isinstance(self.lastLoyaltyUpdate,str):
      #print(f"{self.name}: {self.lastLoyaltyUpdate}")
      #dt = self.lastLoyaltyUpdate.split('.')[0].split('+')[0]
      try: 
        self.lastLoyaltyUpdate = datetime.fromisoformat(self.lastLoyaltyUpdate.split('.')[0].split('+')[0].replace("Z",""))
        self.lastLoyaltyUpdate = pytz.utc.localize(self.lastLoyaltyUpdate)
      except:
        print("Failed")
        print(f"{self.name}: {self.lastSkillUpdate}")
      #self.lastLoyaltyUpdate = datetime.fromisoformat(self.lastLoyaltyUpdate.split('.')[0].split('+')[0] + ".000000+00:00")
    if isinstance(self.lastSkillUpdate,str):
      try: 
        self.lastSkillUpdate = datetime.fromisoformat(self.lastSkillUpdate.split('.')[0].split('+')[0].replace("Z",""))
        self.lastSkillUpdate = pytz.utc.localize(self.lastSkillUpdate)
      except:
        print("Failed")
        print(f"{self.name}: {self.lastSkillUpdate}")
      #self.lastSkillUpdate = datetime.fromisoformat(self.lastSkillUpdate.split('.')[0] + ".000000+00:00")

  
  def updateSkill(self,newSkill:int=0):
    if self.currentSkillLvl == newSkill:
      return False, 'The skill lvl of ' + self.name + ' is already at ' + str(newSkill) + ', keep updating your info whenever you reach a new skill lvl.'
    oldSkill = self.currentSkillLvl
    self.currentSkillLvl = int(newSkill)
    self.lastSkillUpdate = datetime.now() + timedelta(hours = -2)
    self.lastSkillUpdate = pytz.utc.localize(self.lastSkillUpdate)
    self.skillData = self.skillData.append({'skill':newSkill,'date':self.lastSkillUpdate},ignore_index=True)
    #Reply content aware
    reply = 'The skill lvl of ' + self.name + ' is updated from ' + str(oldSkill) + ' to ' + str(newSkill) + '. '
    if newSkill - oldSkill > 1 and oldSkill > 0:
      reply += "Please put in every lvl you increase, don't be lazy!"
    elif newSkill - oldSkill < 1 and oldSkill > 0:
      reply += "I see you tried to cheat yourself to the top, glad you realized telling the truth is the better option."
    return True, reply
  
  def updateLoyalty(self,newLoyalty:int=0):
    if self.currentLoyalty == newLoyalty:
      return False, 'The Loyalty of ' + self.name + ' is already at ' + str(newLoyalty) + ', keep updating your info whenever you increase your Loyalty.'
    oldLoyalty = self.currentLoyalty
    self.currentLoyalty = int(newLoyalty)
    self.lastLoyaltyUpdate = datetime.now()+ timedelta(hours = -2)
    self.lastLoyaltyUpdate = pytz.utc.localize(self.lastLoyaltyUpdate)
    self.loyaltyData = self.loyaltyData.append({'loyalty':newLoyalty,'date':self.lastLoyaltyUpdate},ignore_index=True)
    #Reply content aware
    reply = 'The Loyalty of ' + self.name + ' is updated from ' + str(oldLoyalty) + ' to ' + str(newLoyalty) + '.'
    if newLoyalty - oldLoyalty > 100 and newLoyalty - oldLoyalty < 1400 and oldLoyalty > 0:
      reply += "Please put in every loyalty increase, don't be lazy!"
    elif newLoyalty - oldLoyalty <= -1200:
      reply += "Ahh someone needed a respec, keep pushing!"
    elif newLoyalty - oldLoyalty >= 1200 and oldLoyalty > 0:
      reply += "So you made a respec, or did you just forget to update your loyalty the past days? If so shame on you!"
    return True, reply
  
  def firstTimeLoyaltyAbove(self,loy=int):
    if self.loyaltyData.empty:
      return False, 0, datetime.now() + timedelta(hours = -2)
    if self.loyaltyData.loyalty.max() > loy:
      loys = self.loyaltyData[self.loyaltyData['loyalty'].ge(loy)]
      lo = loys['date'].idxmin()
      return True, loys['loyalty'][lo], loys['date'][lo]
    else:
      loys = (self.loyaltyData.sort_values(by=['date'], ascending=True))
      loys['sortLoy'] = [-i for i in loys['loyalty']]
      loys = (loys.sort_values(by=['sortLoy','date'], ascending=True))
      loys.reset_index(drop=True,inplace=True)
      return False, loys['loyalty'][0], loys['date'][0]
  
  def firstTimeSkillAbove(self,skill=int):
    if self.skillData.empty:
      return False, 0, datetime.now() + timedelta(hours = -2)
    if self.skillData.skill.max() > skill:
      vals = self.skillData[self.skillData['skill'].ge(skill)]
      va = vals['date'].idxmin()
      return True, vals['skill'][va], vals['date'][va]
    else:
      vals = (self.skillData.sort_values(by=['date'], ascending=True))
      vals['sortSki'] = [-i for i in vals['skill']]
      vals = (vals.sort_values(by=['sortSki','date'], ascending=True))
      vals.reset_index(drop=True,inplace=True)
      return False, vals['skill'][0], vals['date'][0]


  def historicLoyalty(self,histDate):
    data = self.loyaltyData
    if data.empty:
      return False, 0 , datetime.now()+ timedelta(hours = -2)
    data['deltaTime'] = [i-histDate for i in data.date]
    if min(data['deltaTime']) >= timedelta(days=0):
      #If no old Data is found using oldest available one
      d = data[data.date == data.date.min()]
      idx = d.index.min()
      return False, int(d.loyalty[idx]), d.date[idx]
    d = data[data.deltaTime == max([i for i in data.deltaTime if i < timedelta(days=0)])]
    return True, int(d.loyalty.values[0]), d.date.values[0]
  
  def historicSkill(self,histDate):
    data = self.skillData
    if data.empty:
      return False, 0 , datetime.now()+ timedelta(hours = -2)
    data['deltaTime'] = [i-histDate for i in data.date]
    if min(data['deltaTime']) >= timedelta(days=0):
      #If no old Data is found using oldest available one
      d = data[data.date == data.date.min()]
      idx = d.index.min()
      return False, int(d.skill[idx]), d.date[idx]
    
    d = data[data.deltaTime == max([i for i in data.deltaTime if i < timedelta(days=0)])]
    return True, int(d.skill.values[0]), d.date.values[0]

  def rName(self):
    unwantedChar = ['꧂','꧁','🍀']
    name = self.name
    for c in unwantedChar:
      name = name.replace(c,'')
    return name
  
  def save(self):
    db[sv.db.memberPrefix + str(self.id)] = self.mem2txt()
  


