import nextcord
from operator import attrgetter

from classes.Member import MemberClass

from functions import staticValues as sv
from functions.generalFunc import Ranking2Embeds

#List of all banner accounts
def listBanners(membersList: [MemberClass]):
  #List of all banners
  banners = []
  active = 0
  for b in membersList:
    if b.banner or b.bannerActive:
      banners.append(b)
      if b.bannerActive:
        active += 1
  banners = sorted(banners,key=attrgetter('bannerActive','name','ownerName'))
  bList = banner2Table(banners,256)
  title = 'There are a total of ' + str(len(banners)) + ' banner accounts listed with ' + str(active) + ' specced for flag.'
  description = ''
  header = "**flag?        Name                           Owner**"
  return Ranking2Embeds(bList,title,description,header,nextcord.Color.blue())

def banner2Table(banners,charLimit):
  charLimits = [256,1024]
  i = 1
  results = []
  rMess = '```'
  for b in banners:
    #Is it specced as flag
    a = sv.emoji.false + ' '
    if b.bannerActive:
      a = sv.emoji.check + ' '

    #Banner name (shorten or fill up with white space)
    name = b.name
    while len(name) > 15:
      name = name[:-1]
    while len(name) < 16:
      name += ' '

    #Owner name (shorten or fill up with white space)
    owner = b.ownerName
    print(owner)
    while len(owner) > 12:
      owner = owner[:-1]
    while len(owner) < 12:
      owner += ' '

    #split message if current line is exceeding charLimit
    if len(rMess + a + name + owner + '\n') + 5 >= charLimits[i]:
      rMess += '```'
      results.append(rMess)
      rMess = '```'
      i = 0 if i == 1 else 1
    rMess = rMess + a + name + owner + '\n'
  rMess += '```'
  results.append(rMess)
  return results

