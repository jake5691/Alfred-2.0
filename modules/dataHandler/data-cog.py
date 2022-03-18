from nextcord.ext import commands
from classes.Structure import Structure
from classes.Member import MemberClass
from classes.Season import Season
from classes.Target import Target
from functions import setupFunc as sf
from functions import staticValues as sv
from functions import seasonFunc as sfu
from functions import targetFunctions as tf
from replit import db
from operator import attrgetter
import nextcord
from datetime import datetime, time, tzinfo


class Data(commands.Cog):
  """Setup of the bot, Data Handling especially keeping the members list up to date"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #sf.importStructureCSV()
    self.structures:[Structure] = sf.loadStructures()
    self.strucNames: [str] = self._getStructureNames()
    #Loading members from txt
    #self.members:[MemberClass] = sf.importMemberTXT() 
    #Loading members from Database
    self.members:[MemberClass] = sf.loadMembers() 
    self.seasons:[Season] = sfu.loadSeasons()
    targets:[Target] = tf.loadTargets(self.getFlags())
    self.targets = sorted(targets, key=attrgetter('hour', 'minute'))

    

  
  @commands.Cog.listener('on_ready')
  async def listCommands(self):
    """List all Commands"""
    #game = nextcord.Game(name="Rise of Empire")
    #await self.bot.change_presence(status=nextcord.Status.online, activity=game)
    #print("Do it")
    #coms = self.bot.get_application_commands()
    #print(coms)
    #print(g)
    #print(g.description)


  @commands.Cog.listener('on_ready')
  async def create_MemberInstances(self):
    """Create Member Instance for every Member having a relevant role, delete Member Instance if no relevant role exists"""
    for g in self.bot.guilds:
      if g.id == sv.gIDS[0]: #Only do this for the RBC server
        relevantRoles = [sv.roles.RBC, sv.roles.GuildMember, sv.roles.Newbie]
        #Delete
        cutoffDate = None
        for s in self.seasons:
          if s.closed:
            cutoffDate = s.end
            cutoffDate = datetime.combine(cutoffDate, time())
            #print(cutoffDate)
        for mi in self.members:
          #Delete old Loyalty data
          #print(f"{mi.name}: {mi.currentLoyalty} - {mi.lastLoyaltyUpdate}")
          #for i in mi.loyaltyData.index:
          #  if mi.loyaltyData["date"][i] < cutoffDate:
          #    mi.loyaltyData = mi.loyaltyData.drop([i])
              #print(type(mi.loyaltyData["date"][i]))
              #print(mi.loyaltyData["date"][i])
          #print(mi.loyaltyData["date"])
          #idx = mi.loyaltyData.index
          #if len(idx) == 0:
          #  print(f"NODATA: {mi.name}: {mi.currentLoyalty} - {mi.lastLoyaltyUpdate}")
          #  mi.currentLoyalty = 0
          #  mi.lastLoyaltyUpdate = None
          #  mi.save()
          if mi.banner:
            continue
          mem = next((x for x in g.members if x.id == mi.id), None)
          if mem != None:
            roles = [r.id for r in mem.roles]
            if not(any(r in roles for r in relevantRoles)):
              self.deleteMemberByID(mem.id)
        #Create
        for m in g.members:
          roles = [r.id for r in m.roles]
          if self.getMemberByID(m.id) == None and any(r in roles for r in relevantRoles):
            print(m.name)
            mem = MemberClass(m)
            mem.save()
            self.members.append(mem)
        
        

  def getFlags(self) -> [MemberClass]:
    flags = []
    for m in self.members:
      if m.bannerActive:
        flags.append(m)
    return flags
  
  def getBannerNames(self) -> [str]:
    banner = []
    for m in self.members:
      if m.banner:
        banner.append(m.name)
    return banner

  def deleteBannerByName(self, name=str) -> bool:
    for m in self.members:
      if m.banner and m.name == name:
        self.members.remove(m)
        del db[sv.db.memberPrefix + str(m.id)]
        return True
    return False
  
  def deleteMemberByID(self,id) -> bool:
    for m in self.members:
      if m.id == id:
        self.members.remove(m)
        del db[sv.db.memberPrefix + str(m.id)]
        return True
    return False
  
  def getMemberByID(self,id=int) -> MemberClass:
    member = next((x for x in self.members if x.id == id), None)
    return member
  
  def _getStructureNames(self) -> [str]:
    structNames = []
    for s in self.structures:
      if s.name in structNames:
        continue
      structNames.append(s.name)
    structNames.sort()
    return structNames
  
  def getSeasonNames(self) -> [str]:
    seasons = [s.name for s in self.seasons]
    return seasons
  
  def getSeasonByName(self,name:str) -> Season:
    for s in self.seasons:
      if s.name == name:
        return s
    return None
  


def setup(bot: commands.Bot):
  bot.add_cog(Data(bot))