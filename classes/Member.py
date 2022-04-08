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

    for attr in self.__dict__:
      if "wonder" in attr:
        print(attr)
        setattr(self, attr, getattr(self, attr).to_csv(index=False))
    
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
    for attr in self.__dict__:
      if "wonder" in attr:
        print(attr)
        print(getattr(self, attr))
        setattr(self, attr, pd.read_csv(StringIO(getattr(self, attr)),sep=','))
        for i in getattr(self, attr).index:
          pass
          getattr(self, attr).at[i,'date'] = datetime.fromisoformat(getattr(self, attr)['date'][i].split('.')[0].split('+')[0] + ".000000+00:00")
  
  def updateSkill(self,newSkill:int=0):
    """update the skill/spec lvl"""
    if self.currentSkillLvl == newSkill:
      return False, 'The skill lvl of ' + self.name + ' is already at ' + str(newSkill) + ', keep updating your info whenever you reach a new skill lvl.'
    oldSkill = self.currentSkillLvl
    self.currentSkillLvl = int(newSkill)
    self.lastSkillUpdate = datetime.now() + timedelta(hours = -2)
    self.lastSkillUpdate = pytz.utc.localize(self.lastSkillUpdate)
    addedData = pd.DataFrame(columns=['skill','date'])
    addedData.loc[0] = [newSkill,self.lastSkillUpdate]
    self.skillData = pd.concat(objs= [self.skillData, addedData])
    self.skillData.reset_index(drop=True, inplace=True)
    #self.skillData = self.skillData.append({'skill':newSkill,'date':self.lastSkillUpdate},ignore_index=True)
    #Reply content aware
    reply = 'The skill lvl of ' + self.name + ' is updated from ' + str(oldSkill) + ' to ' + str(newSkill) + '. '
    if newSkill - oldSkill > 1 and oldSkill > 0:
      reply += "Please put in every lvl you increase, don't be lazy!"
    elif newSkill - oldSkill < 1 and oldSkill > 0:
      reply += "I see you tried to cheat yourself to the top, glad you realized telling the truth is the better option."
    return True, reply

  def updateWonder(self, wonderName=str, increment:int=None, lvl:int=None):
    """update the specific Wonder lvl"""
    wonderName = "wonder" + wonderName.replace(" ", "")
    #check if wonder attribute already exists for that Member if not create it 
    wonderDF = getattr(self, wonderName, pd.DataFrame(columns=["lvl","date"]))
    #get the lvl needed to be added
    print(wonderName)
    if increment is not None:
      if wonderDF.empty:
        lvl = increment
      else:
        lvl = wonderDF["lvl"].iat[-1] + increment
    print(lvl)
    #Get current Time
    currentTime = datetime.now() + timedelta(hours = -2)
    currentTime = pytz.utc.localize(currentTime)
    #Add data to Dataframe
    addedData = pd.DataFrame(columns=["lvl","date"])
    addedData.loc[0] = [lvl, currentTime]
    if wonderDF.empty:
      setattr(self, wonderName, addedData)
      return lvl
    wonderDF = pd.concat(objs= [wonderDF, addedData])
    wonderDF.reset_index(drop=True, inplace=True)
    setattr(self, wonderName, wonderDF)
    return lvl
  
  def updateLoyalty(self,newLoyalty:int=0):
    """update the loyalty"""
    if str(newLoyalty)[-1] != "1":
      #make sure the last digit is a 1
      newLoyalty = int(str(newLoyalty)[:-1] + "1")
    if self.currentLoyalty == newLoyalty:
      return False, 'The Loyalty of ' + self.name + ' is already at ' + str(newLoyalty) + ', keep updating your info whenever you increase your Loyalty.'
    oldLoyalty = self.currentLoyalty
    self.currentLoyalty = int(newLoyalty)
    self.lastLoyaltyUpdate = datetime.now()+ timedelta(hours = -2)
    self.lastLoyaltyUpdate = pytz.utc.localize(self.lastLoyaltyUpdate)
    addedData = pd.DataFrame(columns=['loyalty','date'])
    addedData.loc[0] = [newLoyalty,self.lastLoyaltyUpdate]
    self.loyaltyData = pd.concat(objs= [self.loyaltyData, addedData])
    self.loyaltyData.reset_index(drop=True, inplace=True)
    #self.loyaltyData = self.loyaltyData.append({'loyalty':newLoyalty,'date':self.lastLoyaltyUpdate},ignore_index=True)
    #Reply content aware
    reply = 'The Loyalty of ' + self.name + ' is updated from ' + str(oldLoyalty) + ' to ' + str(newLoyalty) + '. '
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
      loys.reset_index(inplace=True)
      #lo = loys['date'].idxmin()
      return True, loys['loyalty'][0], loys['date'][0]
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
      vals.reset_index(inplace=True)
      #va = vals['date'].idxmin()
      return True, vals['skill'][0], vals['date'][0]
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
  


