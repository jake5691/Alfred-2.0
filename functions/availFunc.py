from nextcord import Member, Guild
from functions import staticValues as sv
from nextcord.utils import get

#Remove members from list with an assigned team
def removeTeamAssignees(memberList: [Member], guild: Guild) -> [Member]:
  mList = []
  removeRoles = [
    get(guild.roles, id=sv.roles.TeamFoxtrot),
    get(guild.roles, id=sv.roles.TeamTango),
    get(guild.roles, id=sv.roles.TeamWhiskey)
  ]
  for m in memberList:
    if not(isinstance(m,Member)):
      print(m.name)
      continue
    if any(r in removeRoles for r in m.roles) or m.bot:
      continue
    mList.append(m)
  return mList